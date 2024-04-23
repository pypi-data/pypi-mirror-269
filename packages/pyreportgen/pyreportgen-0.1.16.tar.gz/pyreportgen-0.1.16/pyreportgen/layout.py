
from pyreportgen.base import Component
import pyreportgen.helpers as helpers 


class Box(Component):
    def __init__(self, children: list[Component]=[], color:str="Info"):
        self.children:list[Component] = children
        self.color:str = color
    
    def render(self) -> str:
        html = ""
        for i in self.children:
            html += i.render()
        return helpers.tagwrap(html, "div", f"Box Color{self.color}")

class Empty(Component):
    def __init__(self):
        super().__init__()
    def render(self) -> str:
        return helpers.tagwrap("", "div")

class HBox(Component):
    def __init__(self, children:list[Component]=[], class_list:list[str]=[]):
        super().__init__()
        self.children:list[Component] = children
        self.class_list = class_list
    
    def render(self) -> str:
        html = ""

        for i in self.children:
            html += i.render()

        
        return helpers.tagwrap(html, "div", "HBox "+" ".join(self.class_list))

    
class VBox(Component):
    def __init__(self, children:list[Component]=[], class_list:list[str]=[]):
        super().__init__()
        self.children:list[Component] = children
        self.class_list = class_list
    
    def render(self) -> str:
        html = ""

        for i in self.children:
            html += i.render()

        return helpers.tagwrap(html, "div", "VBox NoBreak "+" ".join(self.class_list))
    
class HCenterContent(Component):
    def __init__(self, child:Component):
        super().__init__()
        self.child:Component = child
    def render(self) -> str:
        return helpers.tagwrap(self.child.render(), "div", "HCenterContent")
    
class PageBreak(Component):
    def __init__(self):
        super().__init__()
    
    def render(self) -> str:
        return helpers.tagwrap("", "div", "PageBreak")
    
class List(Component):
    def __init__(self, elements:list[str], numbered:bool=False, start:int=1):
        super().__init__()
        self.elements:list[str] = elements
        self.numbered:bool = numbered
        self.start:int = start

    def render(self) -> str:
        html = ""
        element = ""
        if self.numbered:
            element = "ol"
        else:
            element = "ul"


        for el in self.elements:
            html += helpers.tagwrap(el, "li")
        
        return helpers.tagwrap(html, element, props=f"start='{self.start}'", classList="List")