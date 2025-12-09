import requests
from typing import List, Dict, Optional
from urllib.parse import urljoin


class WikimediaCommonsVideoFinder:
    """Tool to search Wikimedia Commons for public domain videos."""

    BASE_URL = 'https://commons.wikimedia.org/w/api.php'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'PublicDomainVideoFinder/1.0'})

    def get_category_members(
        self, category: str, member_type: str = 'file', continue_params: Dict = None
    ) -> Dict:
        """Fetch members of a category from Wikimedia Commons."""
        params = {
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': f'Category:{category}',
            'cmlimit': '500',  # Get maximum results per request
            'cmtype': member_type,  # 'file', 'subcat', or 'page'
            'format': 'json',
        }

        # Add continuation parameters if provided
        if continue_params:
            params.update(continue_params)

        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    def get_file_info(self, titles: List[str]) -> Dict:
        """Get detailed information about files including their URLs."""
        params = {
            'action': 'query',
            'titles': '|'.join(titles),
            'prop': 'imageinfo',
            'iiprop': 'url|mime|mediatype',
            'format': 'json',
        }

        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()

    def is_video_file(self, mime_type: str, media_type: str) -> bool:
        """Check if a file is a video based on MIME type and media type."""
        return media_type == 'VIDEO' or mime_type.startswith('video/')

    def search_public_domain_videos(
        self, recursive: bool = True
    ) -> List[Dict[str, str]]:
        """
        Search for all videos in the 'Films_in_the_public_domain' category.

        Args:
            recursive: If True, search subcategories as well

        Returns:
            List of dictionaries containing video information with keys:
            - title: The file title
            - url: Direct URL to the video file
            - mime_type: MIME type of the video
        """
        videos = []
        category = 'Films_in_the_public_domain'
        processed_categories = set()
        categories_to_process = [category]

        print(f'Searching category: {category}')

        while categories_to_process:
            current_category = categories_to_process.pop(0)

            if current_category in processed_categories:
                continue

            processed_categories.add(current_category)
            print(f'\n--- Processing category: {current_category} ---')

            # First, get all files in this category
            videos_in_category = self._get_videos_from_category(current_category)
            videos.extend(videos_in_category)

            # If recursive, get subcategories
            if recursive:
                subcats = self._get_subcategories(current_category)
                if subcats:
                    print(f'Found {len(subcats)} subcategories')
                    categories_to_process.extend(subcats)

        return videos

    def _get_subcategories(self, category: str) -> List[str]:
        """Get all subcategories of a category."""
        subcategories = []
        continue_params = None

        while True:
            data = self.get_category_members(
                category, member_type='subcat', continue_params=continue_params
            )

            members = data.get('query', {}).get('categorymembers', [])
            for member in members:
                # Remove 'Category:' prefix
                subcat_name = member['title'].replace('Category:', '')
                subcategories.append(subcat_name)

            if 'continue' in data:
                continue_params = data['continue']
            else:
                break

        return subcategories

    def _get_videos_from_category(self, category: str) -> List[Dict[str, str]]:
        """Get all video files from a single category."""
        videos = []
        continue_params = None
        page_count = 0

        while True:
            page_count += 1
            data = self.get_category_members(
                category, member_type='file', continue_params=continue_params
            )

            members = data.get('query', {}).get('categorymembers', [])
            print(f'  Page {page_count}: Retrieved {len(members)} files')

            if not members:
                break

            # Process in batches (API allows up to 50 titles at once)
            batch_size = 50
            titles = [member['title'] for member in members]

            for i in range(0, len(titles), batch_size):
                batch = titles[i : i + batch_size]
                file_info = self.get_file_info(batch)

                pages = file_info.get('query', {}).get('pages', {})
                for page_id, page_data in pages.items():
                    if 'imageinfo' not in page_data:
                        continue

                    image_info = page_data['imageinfo'][0]
                    mime_type = image_info.get('mime', '')
                    media_type = image_info.get('mediatype', '')

                    # Filter for videos only
                    if self.is_video_file(mime_type, media_type):
                        videos.append(
                            {
                                'title': page_data['title'],
                                'url': image_info.get('url', ''),
                                'mime_type': mime_type,
                            }
                        )
                        print(f'    ✓ Found video: {page_data["title"]}')

            # Check if there are more results
            if 'continue' in data:
                continue_params = data['continue']
            else:
                break

        print(f'  Total videos in this category: {len(videos)}')
        return videos


def main():
    """Example usage of the WikimediaCommonsVideoFinder."""
    finder = WikimediaCommonsVideoFinder()

    try:
        videos = finder.search_public_domain_videos()

        print(f'\n{"=" * 80}')
        print(f'Found {len(videos)} public domain videos')
        print(f'{"=" * 80}\n')

        for i, video in enumerate(videos, 1):
            print(f'{i}. {video["title"]}')
            print(f'   URL: {video["url"]}')
            print(f'   Type: {video["mime_type"]}')
            print()

        return videos

    except requests.RequestException as e:
        print(f'Error fetching data from Wikimedia Commons: {e}')
        return []


if __name__ == '__main__':
    main()
