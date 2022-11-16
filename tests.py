from scraping import Scraping
import unittest

#Les tests sont effectués pour la vidéo de Pierre Niney et HugoDécrypte

class TestScrapingMethods(unittest.TestCase):

    def test_titre(self : object):
        s = Scraping()
        s.focusId("fmsoym8I-3o")
        expectedTitre = "Pierre Niney : L’interview face cachée par HugoDécrypte"
        expectedAuteur = "HugoDécrypte"
        expectedId = "fmsoym8I-3o"
        titre, auteur, idVideo = s.findTitreAuteurId()
        self.assertEqual(titre, expectedTitre)
        self.assertEqual(auteur, expectedAuteur)
        self.assertEqual(idVideo, expectedId)

    def test_jaime(self : object):
        s = Scraping()
        s.focusId("fmsoym8I-3o")
        print("Testons la méthode findJaime :", s.findJaime())

    def test_desc(self : object):
        s = Scraping()
        s.focusId("fmsoym8I-3o")
        print("Testons la méthode findDescription :", s.findDescription())

    def test_liens(self : object):
        s = Scraping()
        s.focusId("fmsoym8I-3o")
        print("Testons la méthode findLiens :", s.findLiens(s.findDescription()))

    def test_comm(self : object):
        s = Scraping()
        s.focusId("fmsoym8I-3o")
        print("Testons la méthode findCommentaires :", s.findCommentaires())
