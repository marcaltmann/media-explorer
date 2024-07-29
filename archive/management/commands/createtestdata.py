import datetime
import json
from pathlib import Path

from django.db import transaction
from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone
from django.contrib.auth import get_user_model

from archive.models import (
    Agent,
    Agency,
    MediaFile,
    Resource,
    Collection,
    MetadataKey,
    EntityReference,
)
from entities.models import Entity
from materials.models import Transcript

User = get_user_model()


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, MediaFile, Agent, Resource, Entity, Collection, MetadataKey]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        create_users()
        create_agents()
        create_resources()
        create_agencies()
        create_transcripts()
        create_entities_kende()
        create_entities_malkovich()
        create_collections()


def create_users():
    User.objects.create_user("alice", "alice@example.com", "password")
    User.objects.create_user("bob", "bob@example.com", "password", is_staff=True)
    User.objects.create_superuser("carol", "carol@example.com", "password")


def create_agents():
    """Creates agent records."""
    Agent.objects.create(
        first_name="Marc",
        last_name="Delomez",
        date_of_birth=datetime.date(1954, 9, 5),
        gender="M",
    )
    Agent.objects.create(
        first_name="Michael",
        last_name="Kende",
        date_of_birth=datetime.date(1974, 3, 13),
        gender="M",
        gnd_id="171121503",
    )
    Agent.objects.create(
        first_name="John",
        last_name="Malkovich",
        date_of_birth=datetime.date(1953, 12, 9),
        gender="M",
        gnd_id="128617381",
    )
    Agent.objects.create(
        first_name="Minoru",
        last_name="Arakawa",
        date_of_birth=datetime.date(1946, 9, 3),
        gender="M",
        gnd_id="",
    )
    Agent.objects.create(
        first_name="Maximilian",
        last_name="Schönherr",
        date_of_birth=datetime.date(1954, 12, 27),
        gender="M",
        gnd_id="130608939",
    )
    Agent.objects.create(
        first_name="貝兒",
        last_name="陳",
        date_of_birth=datetime.date(1990, 3, 14),
        gender="F",
        gnd_id="",
        eastern_name_order=True,
    )


def create_resources():
    """Creates resource records."""
    kende_interview = Resource.objects.create(
        title="Michael Kende (Internet Society)", public=True
    )
    kende_media_file = MediaFile.objects.create(
        resource=kende_interview,
        media_type="video/webm",
        media_url="https://upload.wikimedia.org/wikipedia/commons/transcoded/6/6d/Internet_Hall_of_Fame_2014_Michael_Kende_interview.webm/Internet_Hall_of_Fame_2014_Michael_Kende_interview.webm.720p.vp9.webm",
        poster="doggy.jpg",
        production_date=datetime.datetime(
            2024, 3, 8, 12, 6, 35, tzinfo=get_current_timezone()
        ),
        duration=datetime.timedelta(minutes=3, seconds=55),
    )

    malkovich_interview = Resource.objects.create(
        title="John Malkovich",
        public=True,
    )
    malkovich_media_file = MediaFile.objects.create(
        resource=malkovich_interview,
        media_type="video/webm",
        media_url="https://upload.wikimedia.org/wikipedia/commons/7/74/John_Malkovich_-_Les_Liaisons_dangereuses.webm",
        poster="doggy.jpg",
        production_date=datetime.datetime(
            2024, 3, 9, 7, 42, 22, tzinfo=get_current_timezone()
        ),
        duration=datetime.timedelta(minutes=7, seconds=11),
    )

    arakawa_interview = Resource.objects.create(
        title="Minoru Arakawa (Nintendo)",
        public=True,
    )
    arakawa_media_file = MediaFile.objects.create(
        resource=arakawa_interview,
        media_type="audio/mp3",
        media_url="https://upload.wikimedia.org/wikipedia/commons/5/5c/Minoru_Arakawa_%E2%80%93_Nintendo_%E2%80%93_Gameboy%2C_interviewed_by_Maximilian_Sch%C3%B6nherr_1990.mp3",
        poster="",
        production_date=datetime.datetime(
            2024, 3, 14, 17, 38, 53, tzinfo=get_current_timezone()
        ),
        duration=datetime.timedelta(minutes=3, seconds=46),
    )

    chen_interview = Resource.objects.create(
        title="灣區青年說 · 對話香港 TVB 主持人陳貝兒",
        public=True,
    )
    chen_media_file = MediaFile.objects.create(
        resource=chen_interview,
        media_type="audio/ogg",
        media_url="https://upload.wikimedia.org/wikipedia/commons/2/2a/%E7%81%A3%E5%8D%80%E9%9D%92%E5%B9%B4%E8%AA%AA_%C2%B7_%E5%B0%8D%E8%A9%B1%E9%A6%99%E6%B8%AF_TVB_%E4%B8%BB%E6%8C%81%E4%BA%BA%E9%99%B3%E8%B2%9D%E5%85%92.ogg",
        poster="",
        production_date=datetime.datetime(
            2024, 3, 14, 19, 27, 51, tzinfo=get_current_timezone()
        ),
        duration=datetime.timedelta(minutes=42, seconds=4),
    )

    time_machine = Resource.objects.create(
        title="The Time Machine",
        public=True,
    )
    time_machine_media_file_01 = MediaFile.objects.create(
        resource=time_machine,
        media_type="audio/mp3",
        media_url="https://ia902804.us.archive.org/13/items/timemachine_sjm_librivox/timemachine_01_wells.mp3",
        poster="",
        production_date=datetime.datetime(
            2011, 8, 9, 0, 0, 0, tzinfo=get_current_timezone()
        ),
        duration=datetime.timedelta(minutes=21, seconds=20),
    )


def create_agencies():
    kende_interview = Resource.objects.get(title__startswith="Michael Kende")
    malkovich_interview = Resource.objects.get(title__startswith="John Malkovich")
    arakawa_interview = Resource.objects.get(title__startswith="Minoru Arakawa")
    kende = Agent.objects.get(last_name="Kende")
    malkovich = Agent.objects.get(last_name="Malkovich")
    delomez = Agent.objects.get(last_name="Delomez")
    schoenherr = Agent.objects.get(last_name="Schönherr")
    arakawa = Agent.objects.get(last_name="Arakawa")

    Agency.objects.bulk_create(
        [
            Agency(
                resource=kende_interview,
                agent=kende,
                type=Agency.INTERVIEWEE,
            ),
            Agency(
                resource=malkovich_interview,
                agent=malkovich,
                type=Agency.INTERVIEWEE,
            ),
            Agency(
                resource=malkovich_interview,
                agent=delomez,
                type=Agency.INTERVIEWER,
            ),
            Agency(
                resource=arakawa_interview,
                agent=arakawa,
                type=Agency.INTERVIEWEE,
            ),
            Agency(
                resource=arakawa_interview,
                agent=schoenherr,
                type=Agency.INTERVIEWER,
            ),
        ]
    )


def create_transcripts():
    """Creates transcripts for resources."""
    dir = Path(__file__).parent

    kende_interview = Resource.objects.get(title__startswith="Michael Kende")
    kende_media_file = kende_interview.media_files.first()
    with open(dir / "transcript_kende_en.json") as f:
        kende_transcript = json.load(f)
    malkovich_interview = Resource.objects.get(title__startswith="John Malkovich")
    malkovich_media_file = malkovich_interview.media_files.first()
    with open(dir / "transcript_malkovich_fr.json") as f:
        malkovich_transcript = json.load(f)
    chen_interview = Resource.objects.get(title__startswith="灣區")
    chen_media_file = chen_interview.media_files.first()
    time_machine = Resource.objects.get(title__startswith="The Time Machine")
    time_machine_media_file = time_machine.media_files.first()
    with open(dir / "transcript_chen_en.json") as f:
        chen_transcript = json.load(f)
    with open(dir / "subtitles_chen_en.vtt") as f:
        chen_subtitles = f.read()
    with open(dir / "transcript_timemachine_01_en.json") as f:
        timemachine_01_transcript = json.load(f)

    Transcript.objects.bulk_create(
        [
            Transcript(
                media_file=kende_media_file,
                json=kende_transcript,
                vtt="WEBVTT\r\n\r\n1\r\n00:00:00.189 --> 00:00:07.593\r\nWell, I'm an economist and in the late 90s I was working for the FCC, the Federal Communications Commission in the United States.\r\n\r\n2\r\n00:00:08.494 --> 00:00:13.476\r\nAnd there was a series of mergers that took place between the big internet backbones of the time.\r\n\r\n3\r\n00:00:14.077 --> 00:00:19.760\r\nNow a lot of them don't exist or they were bought up at MCI, WorldCom, UUNet, Sprint.\r\n\r\n4\r\n00:00:20.740 --> 00:00:30.394\r\nAnd so I got involved in looking at the antitrust implications of those mergers, but that really led me into the whole area of internet interconnection,\r\n\r\n5\r\n00:00:30.394 --> 00:00:47.607\r\nbecause what was interesting at the time, and is still true today, is that these companies operated fiber optics and wires across the country, and when they sent telephone calls over them, they were regulated, and when they sent internet traffic over them, they weren't.\r\n\r\n6\r\n00:00:48.567 --> 00:00:52.051\r\nAnd we wanted to make sure it stayed that way throughout the mergers.\r\n\r\n7\r\n00:00:52.711 --> 00:00:59.318\r\nAnd so I really got interested in how these guys could interconnect without regulation on the mergers.\r\n\r\n8\r\n00:00:59.338 --> 00:01:02.141\r\nThat's one of the topics I've stuck to.\r\n\r\n9\r\n00:01:02.481 --> 00:01:10.189\r\nThen I went into consulting, did a number of interesting projects for the Internet Society, and then I joined last August as the chief economist.\r\n\r\n10\r\n00:01:18.097 --> 00:01:32.217\r\nWell I think that really it's again this interconnection issue that when I was at the FCC I wrote this paper called The Digital Handshake that really talked about how this interconnection could work and self-regulate.\r\n\r\n11\r\n00:01:34.159 --> 00:01:38.222\r\nOn the Internet using the same wires as they were regulated on, as I said.\r\n\r\n12\r\n00:01:39.323 --> 00:01:45.888\r\nBut really, it was one of the first papers that really documented why the FCC and why one shouldn't regulate this.\r\n\r\n13\r\n00:01:46.589 --> 00:01:48.090\r\nAnd I've really been building on that.\r\n\r\n14\r\n00:01:48.170 --> 00:01:53.754\r\nAnd even as the system has evolved over the last 12, 13 years, it's really stayed the same.\r\n\r\n15\r\n00:01:53.814 --> 00:02:00.619\r\nAnd so I'm quite proud of that one because it really showed how the Internet could work without regulation.\r\n\r\n16\r\n00:02:00.639 --> 00:02:02.701\r\nI think it's remained true today.\r\n\r\n17\r\n00:02:11.141 --> 00:02:16.766\r\nWell, I think it's overall sunny, but some snowed in clouds, I guess.\r\n\r\n18\r\n00:02:18.447 --> 00:02:28.335\r\nClearly there's some issues, but I think there's general optimism that things are looking good and there's bright sunny days ahead.\r\n\r\n19\r\n00:02:35.936 --> 00:02:38.018\r\nI think it's more hopes than concerns.\r\n\r\n20\r\n00:02:38.238 --> 00:02:43.603\r\nI think that the really exciting thing, we're about to hit 3 billion users by one count.\r\n\r\n21\r\n00:02:43.683 --> 00:02:44.884\r\nIt should happen in June.\r\n\r\n22\r\n00:02:46.266 --> 00:02:49.909\r\nSo that's an amazing number, but that's still about 40% of the world.\r\n\r\n23\r\n00:02:50.790 --> 00:02:56.455\r\nSo I think that one of the things the Internet Society stands for is the Internet is for everyone.\r\n\r\n24\r\n00:02:56.495 --> 00:03:07.112\r\nAnd I think that with the mobile technology we're really going to hit four or five billion soon and I think that's the really exciting prospect that keeps me going.\r\n\r\n25\r\n00:03:16.127 --> 00:03:20.708\r\nWell, I think we have to address the privacy and security issues that have come up.\r\n\r\n26\r\n00:03:20.988 --> 00:03:25.249\r\nI think that, you know, so much of what we're doing in our lives, we're putting on the Internet.\r\n\r\n27\r\n00:03:26.209 --> 00:03:30.990\r\nAnd we have to be sure that the things that we want to remain private remain private.\r\n\r\n28\r\n00:03:31.030 --> 00:03:33.771\r\nWhen we want to be anonymous, it remains anonymous.\r\n\r\n29\r\n00:03:33.831 --> 00:03:40.072\r\nSo I think that we need a simple and easy way to protect our information and make sure it stays safe.\r\n\r\n30\r\n00:03:41.352 --> 00:03:47.478\r\nAs we increasingly put our lives online, as we increasingly interact with our banks, with our government, with everything online.\r\n\r\n31\r\n00:03:47.498 --> 00:03:53.605\r\nSo I think that that's going to have to be addressed, and I'm sure it will be, and the Internet Society will play its part.",
                language="en",
            ),
            Transcript(
                media_file=malkovich_media_file,
                json=malkovich_transcript,
                vtt="WEBVTT\r\n\r\n1\r\n00:00:04.708 --> 00:00:10.011\r\nÇa c'est Paris, à le plaisir d'accueillir dans sa chronique vidéo John Malkovich.\r\n\r\n2\r\n00:00:10.051 --> 00:00:11.311\r\nBonjour.\r\n\r\n3\r\n00:00:11.351 --> 00:00:18.895\r\nAlors, après Goutte Canary, pièce pour laquelle vous avez remporté le Molière de la mise en scène, on vous retrouve au Théâtre de l'Atelier.\r\n\r\n4\r\n00:00:20.277 --> 00:00:27.721\r\nPour une mise en scène de l'adaptation théâtrale de Christopher Hampton, « Des liaisons dangereuses ».\r\n\r\n5\r\n00:00:27.761 --> 00:00:33.364\r\nAlors, vous y pensiez depuis longtemps, à faire cette mise en scène pour cette création ?\r\n\r\n6\r\n00:00:33.424 --> 00:00:35.245\r\nOui, absolument.\r\n\r\n7\r\n00:00:35.285 --> 00:00:39.608\r\nJ'avais lu la pièce, je crois que c'était « Craterman 4 », ça fait très longtemps.\r\n\r\n8\r\n00:00:39.668 --> 00:00:39.768\r\nOui.\r\n\r\n9\r\n00:00:40.208 --> 00:00:43.410\r\nEt j'avais toujours pensé de faire une mise en scène.\r\n\r\n10\r\n00:00:44.430 --> 00:00:58.416\r\nPeut-être pas exactement de la même façon qu'on fait maintenant, mais parce qu'au début, on a eu des autres idées pour la mise en scène et tout ça.\r\n\r\n11\r\n00:00:58.456 --> 00:01:09.880\r\nMais en fait, je suis très content qu'on n'ait pas fait comme on a prévu à l'époque et qu'on a fait la pièce comme on fait maintenant.\r\n\r\n12\r\n00:01:10.407 --> 00:01:12.349\r\nParce qu'au début, c'était totalement différent ?\r\n\r\n13\r\n00:01:12.569 --> 00:01:14.510\r\nTotalement différent, oui.\r\n\r\n14\r\n00:01:14.550 --> 00:01:15.071\r\nComplètement.\r\n\r\n15\r\n00:01:15.091 --> 00:01:17.113\r\nBeaucoup plus lourd.\r\n\r\n16\r\n00:01:17.153 --> 00:01:17.733\r\nBeaucoup plus lourd ?\r\n\r\n17\r\n00:01:18.053 --> 00:01:18.414\r\nOui.\r\n\r\n18\r\n00:01:18.454 --> 00:01:19.034\r\nD'accord.\r\n\r\n19\r\n00:01:19.294 --> 00:01:22.377\r\nCher et pas mal d'autres choses.\r\n\r\n20\r\n00:01:23.346 --> 00:01:23.726\r\nD'accord.\r\n\r\n21\r\n00:01:23.786 --> 00:01:36.115\r\nEt alors, au tout début, généralement, quand on décide de faire une création, on visualise les personnages, les acteurs avec qui on aimerait qu'on voit bien dans tel ou tel rôle.\r\n\r\n22\r\n00:01:36.135 --> 00:01:40.038\r\nVous pensiez à qui au tout début pour Valmont ou Madame de Merteuil ?\r\n\r\n23\r\n00:01:41.219 --> 00:01:54.521\r\nOn a pensé, comme j'avais adoré de travailler avec Christiane Aureli sur Good Community, au début j'avais parlé avec Vincent Cassel pour Valmont,\r\n\r\n24\r\n00:01:54.521 --> 00:01:59.659\r\nj'avais parlé avec Christiane, bien sûr, pour Merteuil.\r\n\r\n25\r\n00:02:06.544 --> 00:02:08.245\r\nBeaucoup d'écoles ?\r\n\r\n26\r\n00:02:38.210 --> 00:02:44.756\r\nTous les conservatoires partout, et par les autres moyens aussi.\r\n\r\n27\r\n00:02:44.836 --> 00:02:52.182\r\nEt comme ça, on a trouvé une troupe splendide.\r\n\r\n28\r\n00:02:52.242 --> 00:02:52.903\r\nExactement, oui.\r\n\r\n29\r\n00:02:53.573 --> 00:03:10.250\r\nVous avez tiré de tous les gens que vous avez vu, vous en avez vu au moins 300 apprentis comédiens ou jeunes comédiens, et il a fallu en filtrer une quinzaine.\r\n\r\n30\r\n00:03:10.270 --> 00:03:11.992\r\nLe choix était difficile ?\r\n\r\n31\r\n00:03:12.032 --> 00:03:13.293\r\nTerriblement difficile.\r\n\r\n32\r\n00:03:15.347 --> 00:03:18.228\r\nEt ça, c'est aucune réflexion.\r\n\r\n33\r\n00:03:18.248 --> 00:03:22.128\r\nLes gens que j'avais choisis, évidemment.\r\n\r\n34\r\n00:03:22.148 --> 00:03:24.729\r\nParce que c'est eux qui étaient choisis.\r\n\r\n35\r\n00:03:24.749 --> 00:03:28.730\r\nMais j'ai eu pas mal de choix, et de très bons choix.\r\n\r\n36\r\n00:03:28.810 --> 00:03:34.471\r\nEt c'était une décision que je ne regrette rien.\r\n\r\n37\r\n00:03:34.511 --> 00:03:38.492\r\nMais quand même, c'était un choix difficile.\r\n\r\n38\r\n00:03:38.512 --> 00:03:41.532\r\nSimplement pour m'apporter une lettre, mais ce n'était pas le cas.\r\n\r\n39\r\n00:03:41.572 --> 00:03:44.933\r\nLorsqu'enfin j'ai compris pourquoi il était là, c'était trop tard.\r\n\r\n40\r\n00:03:55.213 --> 00:03:58.114\r\nC'est carrément une nouvelle traduction.\r\n\r\n41\r\n00:03:58.154 --> 00:04:00.556\r\nOui, oui, complètement.\r\n\r\n42\r\n00:04:00.576 --> 00:04:01.176\r\nD'accord.\r\n\r\n43\r\n00:04:01.236 --> 00:04:02.216\r\nRien n'a été rajouté ?\r\n\r\n44\r\n00:04:04.377 --> 00:04:09.020\r\nOui, mais ça, ça fait partie de l'adaptation.\r\n\r\n45\r\n00:04:09.040 --> 00:04:09.440\r\nÇa veut dire...\r\n\r\n46\r\n00:04:10.919 --> 00:04:23.348\r\nOn n'a pas pris la dernière scène de la vraie pièce de Christopher Hampton, et on a réécrit la dernière, je ne sais pas, trois,\r\n\r\n47\r\n00:04:23.348 --> 00:04:44.390\r\ncinq minutes, quelque chose qui n'existe pas dans la pièce, et qui fait soit partie du scénario de film de Christopher Hampton, où il a fait le scénario pour un film qui porte le même nom, ou qui viennent du roman.\r\n\r\n48\r\n00:04:44.971 --> 00:04:52.860\r\nEn tout cas, c'est une belle initiative du Théâtre de l'Atelier d'avoir accueilli... Oui, et j'adore ce théâtre.\r\n\r\n49\r\n00:04:52.900 --> 00:05:35.442\r\nJ'ai rencontré Laura Pelz, manager en fait et on a discuté le truc c'était plutôt vite fait et on a répété là-bas en 2008 on a fait quelque chose pour la tournée de Good Canary parce que j'étais obligé de refaire un peu le casting et tout ça parce qu'on n'a pas eu tellement de monde sur la tournée mais c'était Vite fait.\r\n\r\n50\r\n00:05:35.462 --> 00:05:39.085\r\nC'est un très joli théâtre.\r\n\r\n51\r\n00:05:39.125 --> 00:05:44.029\r\nC'est extrêmement bien joué, la mise en scène est très bien faite et franchement c'est émouvant et on rigole.\r\n\r\n52\r\n00:05:44.089 --> 00:05:50.714\r\nIl y a des anachronismes qui sont superbes aussi avec l'utilisation d'objets tous les jours dans un décor ancien.\r\n\r\n53\r\n00:05:50.895 --> 00:05:52.616\r\nFranchement, je recommande.\r\n\r\n54\r\n00:05:52.696 --> 00:05:54.057\r\nUn très beau respect du texte.\r\n\r\n55\r\n00:05:55.198 --> 00:06:04.081\r\nUne bonne pêche, une bonne énergie pour les jeunes comédiens et merci John Malkovich de donner la chance aux jeunes comédiens parce que c'est pas toujours le cas.\r\n\r\n56\r\n00:06:04.221 --> 00:06:10.083\r\nFaire profiter de son notoriété pour connaître des nouveaux acteurs, c'est une réussite.\r\n\r\n57\r\n00:06:10.123 --> 00:06:21.787\r\nC'était très intéressant comme réécriture parce que ça change beaucoup du film justement et c'est sympa de pouvoir faire la comparaison entre les deux et là je trouve que le côté humoristique il est bien joué et c'est super sympa.\r\n\r\n58\r\n00:06:21.807 --> 00:06:23.488\r\nVous savez ce que c'est qu'un comité d'entreprise ?\r\n\r\n59\r\n00:06:25.229 --> 00:06:32.181\r\nD'accord, non mais je pose la question, parce que bon voilà, cette vidéo est destinée aux élus de comités d'entreprise, donc voilà,\r\n\r\n60\r\n00:06:32.181 --> 00:06:34.517\r\nqui amènent le public notamment au théâtre.\r\n\r\n61\r\n00:06:35.418 --> 00:06:39.741\r\nAlors pour conclure, je dirais, que ça se passe ?\r\n\r\n62\r\n00:06:39.781 --> 00:06:46.000\r\nJe dirais à mes élus de comités d'entreprise, ça se passe au théâtre de l'atelier, ça s'appelle les liaisons dangereuses,\r\n\r\n63\r\n00:06:46.000 --> 00:06:53.196\r\nc'est signé pour la mise en scène par John Malkovich, Et c'est un des meilleurs spectacles à l'affiche des théâtres parisiens en ce moment.\r\n\r\n64\r\n00:06:53.236 --> 00:06:57.822\r\nVoilà, merci beaucoup, merci John pour ces moments passés en votre compagnie.\r\n\r\n65\r\n00:06:57.842 --> 00:06:58.243\r\nMerci.",
                language="fr",
            ),
            Transcript(
                media_file=chen_media_file,
                json=chen_transcript,
                vtt=chen_subtitles,
                language="en",
            ),
            Transcript(
                media_file=time_machine_media_file,
                json=timemachine_01_transcript,
                language="en",
            ),
        ]
    )


def create_entities_kende():
    """Creates entity records for Kende interview."""
    kende_interview = Resource.objects.get(title__startswith="Michael Kende")

    usa = Entity.objects.create(type=Entity.TYPE_LOCATION, name="USA")
    fcc = Entity.objects.create(
        type=Entity.TYPE_ORGANISATION,
        name="Federal Communications Commission",
        gnd_id="16300677-5",
    )
    internet_society = Entity.objects.create(
        type=Entity.TYPE_ORGANISATION,
        name="Internet Society",
        gnd_id="5174445-4",
    )
    mci = Entity.objects.create(
        type=Entity.TYPE_ORGANISATION, name="MCI Communications"
    )
    sprint = Entity.objects.create(
        type=Entity.TYPE_ORGANISATION, name="Sprint Corporation"
    )
    uunet = Entity.objects.create(type=Entity.TYPE_ORGANISATION, name="UUNET")
    world_com = Entity.objects.create(
        type=Entity.TYPE_ORGANISATION, name="MCI WorldCom"
    )
    paper = Entity.objects.create(type=Entity.TYPE_MISC, name="The Digital Handshake")

    manager = kende_interview.entityreference_set
    manager.create(entity=usa, timecodes=[0.189])
    manager.create(entity=fcc, timecodes=[0.189, 78.097, 99.323])
    manager.create(entity=internet_society, timecodes=[62.481, 227.498])
    manager.create(entity=mci, timecodes=[14.077])
    manager.create(entity=sprint, timecodes=[14.077])
    manager.create(entity=uunet, timecodes=[14.077])
    manager.create(entity=world_com, timecodes=[14.077])
    manager.create(entity=paper, timecodes=[78.097])


def create_entities_malkovich():
    """Creates entity records for Malkovich interview."""
    malkovich_interview = Resource.objects.get(title__startswith="John Malkovich")

    theatre = Entity.objects.create(
        type=Entity.TYPE_LOCATION, name="Théâtre de l'Atelier"
    )
    good_canary = Entity.objects.create(type=Entity.TYPE_MISC, name="Good Canary")
    hampton = Entity.objects.create(
        type=Entity.TYPE_PERSON,
        name="Christopher Hampton",
        gnd_id="118720198",
        description="Sir Christopher James Hampton CBE FRSL (Horta, Azores, 26 January 1946) is a British playwright, screenwriter, translator and film director. He is best known for his play Les Liaisons Dangereuses based on the novel of the same name and the film adaptation. He has thrice received nominations for the Academy Award for Best Adapted Screenplay: for Dangerous Liaisons (1988), Atonement (2007) and The Father (2020); winning for the former and latter.",
    )
    malkovich = Entity.objects.create(
        type=Entity.TYPE_PERSON,
        name="John Malkovich",
        gnd_id="128617381",
        extra={"date_of_birth": "1953-12-09", "sex": "M"},
    )
    cassel = Entity.objects.create(type=Entity.TYPE_PERSON, name="Vincent Cassel")

    manager = malkovich_interview.entityreference_set
    manager.create(entity=theatre, timecodes=[11.351, 284.971])
    manager.create(entity=good_canary, timecodes=[11.351, 101.219, 292.9])
    manager.create(entity=hampton, timecodes=[20.277, 250.919, 263.348])
    manager.create(entity=malkovich, timecodes=[4.708, 355.198, 406.0, 413.236])
    manager.create(entity=cassel, timecodes=[101.219])


def create_collections():
    """Creates example collections and adds resources to them."""
    malkovich_interview = Resource.objects.get(title__startswith="John Malkovich")
    kende_interview = Resource.objects.get(title__startswith="Michael Kende")
    chen_interview = Resource.objects.get(title__startswith="灣區")
    arakawa_interview = Resource.objects.get(title__startswith="Minoru Arakawa")
    time_machine = Resource.objects.get(title__startswith="The Time Machine")

    video_interviews = Collection.objects.create(
        name="Video Interviews",
        description="A collection of video interviews",
    )
    video_interviews.resources.add(kende_interview, malkovich_interview)

    audio_interviews = Collection.objects.create(
        name="Audio interviews",
        description="A collection of audio interviews",
    )
    audio_interviews.resources.add(arakawa_interview, chen_interview)

    internet_collection = Collection.objects.create(
        name="Internet Collection",
        description="A collection of resources about the internet",
    )
    internet_collection.resources.add(kende_interview)

    audio_books_collection = Collection.objects.create(
        name="Audio Books",
        description="A collection of audio books",
    )
    audio_books_collection.resources.add(time_machine)
