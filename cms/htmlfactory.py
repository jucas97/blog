from bs4 import BeautifulSoup

class Factory():

    DivTagClassAttrKey     = "class"
    DivTagContentAttrValue = "content"
    routeTemplate          = "\n@routes.route('/blog/title')\ndef titleget():\n    return render_template('title.html')\n"

    def __init__(self, parent: object, htmlTemplateFilename: str = None, rawData: dict = None) -> None:
        # Guards missing
        self.htmlTemplateFilename = htmlTemplateFilename
        self.rawData = rawData
        self.parent = parent

    def generate(self, htmlTargetPath = None, targetRouteFile: str = None) -> bool:
        if htmlTargetPath == None or targetRouteFile == None:
            return False

        with open(self.htmlTemplateFilename, mode="r") as baseFile:
            fileContent = baseFile.read()
            docHTML = BeautifulSoup(fileContent, "html.parser")

            docHTML("h2")[0].string = self.rawData["title"]
            self.__parseContent(docHTML, self.rawData["content"])

            baseFilename = self.rawData["title"].replace(" ", "")

            with open(htmlTargetPath + "/" + baseFilename + ".html", "w") as htmlFile:
                htmlFile.write(docHTML.prettify())

            with open(targetRouteFile, "a") as pyFile:
                route = self.routeTemplate.replace("title", baseFilename)
                pyFile.write(route)

            # Drop down menu
            parent = self.rawData["parent"] if "parent" in self.rawData.keys() else None
            self.parent.setDropDown(parent, self.rawData["title"])

        return True

    # TODO - redo __buildTag
    def __parseContent(self, docHTML = None, contentList = None):
        def __buildTag(docHTML, type = "div", attrs = None, content = None) -> object:
            if docHTML == None:
                return None

            tag = docHTML.new_tag(type)
            tag.attrs = attrs
            if type != "div":
                tag.string = content
                return tag

            stTag = __buildTag(docHTML, type="h5", content = content["subtitle"])
            pTag = __buildTag(docHTML, type = "p", content = content["data"])
            tag.append(stTag)
            tag.append(pTag)

            return tag

        if docHTML == None:
            return False

        for content in contentList:
            tag = __buildTag(docHTML, "div", {self.DivTagClassAttrKey:self.DivTagContentAttrValue}, content)
            if tag != None:
                docHTML("div", class_="title")[-1].insert_after(tag)
            else:
                return False

        return True
