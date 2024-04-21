# KivyMD-utils
## description
KivyMD-utils brings some flutter widgets to KivyMD.
Github Url <https://github.com/MilanR312/kivymd-utils>


### CoroutineBuilder

This widget allows to render the result of a Coroutine. It will rerender when the coroutine finishes its work.

example:
```py
class TestApp(MDApp):
    async def generate_number(self):
        await asyncio.sleep(2)
        return "5"

    def build(self):
        self.coroutine = self.generate_number()
        return CoroutineBuilder(
            builder=self.generate_text,
            coroutine=self.coroutine
        )
    
    def generate_text(self, snapshot: CoroutineSnapshot):
        if snapshot.has_data:
            return MDLabel(text = snapshot.data)
        else:
            return MDLabel(text = "calculating")     
```

### RedrawAble

A widget that allows all content to be redrawn when a value changes. This widget differs from properties in that it allows any class to inherit the `NotifyListeners` class and be used in any `RedrawAble`. A new value also does not mean an automatic redraw but can be controled using either the `notify_listeners()` method or by calling redraw()
example:
```py
class Person(NotifyListener):
    def __init__(self, name:str, age: int):
        super().__init__()
        self.name = name
        self.age = age

    def age_up(self):
        self.age += 1
        self.notify_listeners()
    

class App(MDApp):
    def build(self):
        self.person = Person("Joe", 25)

        self.redraw_able= RedrawAble(
            provider=self.person,
            builder=lambda: MDBoxLayout(
                MDLabel(text= f"{self.person.name} is {self.person.age} years old"),
                MDTextButton(
                    text= "age",
                    on_release= lambda x:self.person.age_up()
                ),
                MDTextButton(
                    text="force redraw",
                    on_release= lambda x: self.redraw_able.redraw()
                )
            )
        )
        return self.redraw_able
```

### Router
A basic implementation of [GoRouter](https://pub.dev/packages/go_router) is provided under the router directory. The Router widget provides a ScreenManager implementation that allows vertical and horizontal movement.


To achieve horizontal navigation the router allows swapping pages utilizing the `router.go(<url>)` method. The Route of the most specific `path` will be chosen and displayed

basic example:
```py
from kivymd_utils.router import Router, RouterWidget, Route
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.app import MDApp

ROUTER = Router(
    initial_route="/",
    routes= [
        Route(
            path="/",
            builder=lambda state, *args, **kwargs: MDBoxLayout(
                MDLabel(text= "home screen"),
                MDTextButton(
                    text= "to next screen",
                    on_release= lambda x: kwargs["router"].go("/greet")
                )
            )
        ),
        Route(
            path="/greet",
            builder=lambda state, *args, **kwargs: MDLabel(text= "hello user")
        )
    ]
)
class App(MDApp):
    def build(self):
        return RouterWidget(
            router = ROUTER
        )
    
if __name__=="__main__":
    App().run()
```
Nested Routes can be achieved by nesting routes inside the Router widget.

example:
```py
from kivymd_utils.router import Router, RouterWidget, Route
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.app import MDApp

ROUTER = Router(
    initial_route="/",
    routes= [
        Route(
            path="/",
            builder=lambda state, *args, **kwargs: MDBoxLayout(
                MDLabel(text= "home screen"),
                MDTextButton(
                    text= "to next screen",
                    on_release= lambda x: kwargs["router"].go("/greet")
                )
            )
        ),
        Route(
            path="/greet",
            builder=lambda state, *args, **kwargs: MDBoxLayout(
                MDLabel(text= "hello user"),
                MDTextButton(
                    text= "go deeper",
                    on_release= lambda x: kwargs["router"].go("/greet/again")
                )
            ),
            routes=[
                Route(
                    path="/again",
                    builder=lambda state, *args, **kwargs: MDLabel(text= "hello again")
                )
            ]
        )
    ]
)
class App(MDApp):
    def build(self):
        return RouterWidget(
            router = ROUTER
        )
    
if __name__=="__main__":
    App().run()
```

If you need a topbar for all elements of a specific path you can utilize a ShellRoute. The shellroute draws its own content around the child object.

```py
ROUTER = Router(
    initial_route="/",
    routes= [
        ShellRoute(
            builder=lambda state, child, *args, **kwargs: MDBoxLayout(
                MDLabel(text="Title block"),
                child,
                orientation="vertical"
            ),
            routes=[
                Route(
                    path="/",
                    builder=lambda state, *args, **kwargs: MDBoxLayout(
                        MDLabel(text="home"),
                        MDTextButton(
                            text="next_page",
                            on_release= lambda x: kwargs["router"].go("/greet")
                        )
                    )
                ),
                Route(
                    path="/greet",
                    builder=lambda state, *args, **kwargs: MDLabel(text= "hello user")
                )
            ]
        )
    ]
)
```

When routing sometimes you need to pass an object to the widget to display it. To notify a route passes an object you need to start it with a ':'

example:
```py
ROUTER = Router(
    initial_route="/",
    routes= [
        Route(
            path="/",
            builder=lambda state, *args, **kwargs: MDBoxLayout(
                MDLabel(text="home"),
                MDTextButton(
                    text="go greet",
                    #for simple string objects, we can pass it as a url itself
                    on_release= lambda x: kwargs["router"].go("/greet/Joe")
                ),
                MDTextButton(
                    text="go greet",
                    #you can also pass data with the goData method and a dictionary containing data
                    #the key is equivalent to the name in the url '/greet/:name'
                    #all items are optional in the dictionary and will fall back to the item in the url
                    on_release= lambda x: kwargs["router"].goData("/greet/_", {"name": "Joe"})
                )
            )
        ),
        Route(
            path="/greet/:name",
            #you can access the data via the state.parameters dictionary
            builder=lambda state, *args, **kwargs: MDLabel(text= state.parameters["name"])
        )
    ]
)
```


When a page gets moved to a new route you can modify the old route to be a redirect, this allows all the old `router.go()` methods to point to the new page with minimal configuration.

example:
```py
ROUTER = Router(
    initial_route="/",
    routes= [
        Route(
            path="/",
            builder=lambda state, *args, **kwargs: MDBoxLayout(
                MDLabel(text="home"),
                MDTextButton(
                    text="go greet",
                    on_release= lambda x: kwargs["router"].go("/old")
                ),

            )
        ),
        Route(
            path="/old",
            redirect="/new"
        ),
        Route(
            path="/new",
            builder=lambda state, *args, **kwargs: MDLabel(text= "a new page")
        )
    ]
)
```

To allow for vertical movement the provided methods of `push(<url>)` and `pop()` are provided. An equivalent `pushData(<url>, <data>)` is also provided.
Everytime a `.go()` method is called the current page stack gets cleared. Pushing a page adds it to the current page stack allowing for a back button to call `pop()`

example:
```py
ROUTER = Router(
    initial_route="/",
    routes= [
        Route(
            path="/",
            builder=lambda state, *args, **kwargs: MDBoxLayout(
                MDLabel(text="home"),
                MDTextButton(
                    text="show popup",
                    on_release= lambda x: kwargs["router"].push("/popup")
                ),

            )
        ),
        Route(
            path="/popup",
            builder=lambda state, *args, **kwargs: MDBoxLayout(
                MDLabel(text="popup"),
                MDTextButton(
                    text="go back",
                    on_release= lambda x: kwargs["router"].pop()
                )
            )
        )
    ]
)
```

Instead of a builder method you can also pass a prebuilt widget to the Route. Due to a limitation with kivy itself, this is not possible when declaring the router as a global variable.

example:
```py
class App(MDApp):
    def build(self):
        router = Router(
            initial_route="/",
            routes= [
                Route(
                    path="/",
                    builder=lambda state, *args, **kwargs: MDBoxLayout(
                        MDLabel(text="home"),
                        MDTextButton(
                            text="show prebuilt",
                            on_release= lambda x: kwargs["router"].push("/prebuilt")
                        ),

                    )
                ),
                Route(
                    path="/prebuilt",
                    #you can access the data via the state.parameters dictionary
                    widget=MDLabel(text="prebuilt"),
                )
            ]
        )
        return RouterWidget(
            router = router
        )
```


Using the router in KV files is easy but requires an assignment in the build method.
```kv
<HomePage>
    MDLabel:
        text: "home"
    MDTextButton:
        text: "go to greet"
        on_release: app.router.go("/greet")

<GreetPage>
    MDLabel:
        text: "hello"
    MDTextButton:
        text: "go home"
        on_release: app.router.go("/")
```
with python file
```py
class HomePage(MDBoxLayout):
    pass

class GreetPage(MDBoxLayout):
    pass

ROUTER = Router(
    initial_route="/",
    routes= [
        Route(
            path="/",
            builder=lambda state, *args, **kwargs: HomePage(),
        ),
        Route(
            path="/greet",
            builder=lambda state, *args, **kwargs: GreetPage()
        )
    ]
)

class TestRoutesBase(MDApp):
    def build(self):
        #assignment needed here
        self.router = ROUTER
        return RouterWidget(
            router=ROUTER
        )
```