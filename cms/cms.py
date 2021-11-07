import htmlfactory
import shutil

class CMS:

    def __init__(self, htmlTemplateFilename: str):
        #Guards missing
        self.htmlTemplateFilename = htmlTemplateFilename
        self.htmlFactories = []
        self.dropDown = []

    def createFactories(self, htmlData: list):
        for content in htmlData:
            self.htmlFactories.append(htmlfactory.Factory(self.htmlTemplateFilename, content))

    def generateHTML(self, htmlTargetPath: str, templateFilename: str, targetFilename: str):
        # Truncate routes.py and copy template data, guards missing
        shutil.copyfile(templateFilename, targetFilename)
        for factory in self.htmlFactories:
            factory.generate(htmlTargetPath, targetFilename)
