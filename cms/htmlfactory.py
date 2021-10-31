from bs4 import BeautifulSoup

class HTMLPage():

    DivTagClassAttrKey     = "class"
    DivTagContentAttrValue = "content"

    def __init__(self, targetPath: str = "", rawData: dict = None) -> None:
        self.targetPath = targetPath
        self.rawData = rawData

    def generate(self, filename = None) -> bool:
        with open(filename, mode="r") as baseFile:
            fileContent = baseFile.read()
            docHTML = BeautifulSoup(fileContent, "html.parser")

            for key, value in self.rawData.items():
                # Process parse result - verify possible failures
                if key == "title":
                    self.__parseTitle(docHTML, value)
                elif key == "content":
                    self.__parseContent(docHTML, value)
            print(docHTML.prettify())

    def __parseTitle(self, docHTML = None, title = "N/A") -> bool:
        if docHTML == None:
            return False

        docHTML("h2")[0].string = title

        return True

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
