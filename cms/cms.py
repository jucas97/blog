import htmlfactory
import shutil

class CMS:

    def __init__(self, htmlTemplateFilename: str):
        #Guards missing
        self.htmlTemplateFilename = htmlTemplateFilename
        self.htmlFactories = []
        self.dropDown = []

    def createFactories(self, htmlData: list) -> None:
        for content in htmlData:
            self.htmlFactories.append(htmlfactory.Factory(self, self.htmlTemplateFilename, content))

    def generateHTML(self, htmlTargetPath: str, templateFilename: str, targetFilename: str) -> None:
        # Truncate routes.py and copy template data, guards missing
        shutil.copyfile(templateFilename, targetFilename)
        for factory in self.htmlFactories:
            factory.generate(htmlTargetPath, targetFilename)

    def setDropDown(self, parent: str = "General", title: str = None) -> None:
        if title == None:
            return

        if parent == None:
            parent = "General"

        # Can be optimized
        if any(parent in k for k in self.dropDown):
           [{key:value.append(title)  for (key,value) in d.items() if key==parent  and title not in value} for d in self.dropDown]
        else:
            self.dropDown.append({parent:[title]})
