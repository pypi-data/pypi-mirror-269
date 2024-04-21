from __future__ import annotations

class Color:
    def __init__(self, r: int, g: int, b: int, a: float) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @classmethod
    def from_rgb(cls, r, g, b) -> Color:
        return Color(r,g,b, 1.0)
    
    @classmethod
    def from_hsl(cls, h: float, s: float, l: float) -> Color:
        """h is in degrees
        s,l in %"""
        c = s* (1 - abs(2*l - 1))
        x = c * (1 - abs((h/60) % 2 - 1))
        m = l - c/2

        (r,g,b) = (0,0,0)
        if h < 60:
            (r,g,b) = (c,x,0)
        elif h < 120:
            (r,g,b) = (x,c,0)
        elif h < 180:
            (r,g,b) = (0,c,x)
        elif h < 240:
            (r,g,b) = (0,x,c)
        elif h < 300:
            (r,g,b) = (x,0,c)
        else:
            (r,g,b) = (c,0,x)
        
        return Color(int((r+m)*255),int((g+m)*255),int((b+m)*255),1)
    
    @classmethod
    def from_cmyk(cls, c,m,y,k) -> Color:
        r = 255 * (1-c) * (1-k)
        g = 255 * (1-m) * (1-k)
        b = 255 * (1-y) * (1-k)
        return Color(int(r),int(g),int(b),1)
    
    @classmethod
    def from_hex(cls, hex: str) -> Color:
        assert len(hex) == 6 or len(hex) == 8 #with or without transparency
        r = int(hex[0:2], base=16)
        g = int(hex[2:4], base=16)
        b = int(hex[4:6], base=16)
        a = 1.0 if len(hex) == 6 else int(hex[6:8],base=16)/255
        return Color(r,g,b,a)

    def to_rgb(self) -> tuple[int, int,int]:
        return (self.r, self.g, self.b)
    
    def to_rgb_float(self) -> tuple[float, float, float]:
        """returns rgb values but mapped from 0 to 1.0 instead of 0 to 255"""
        return list(map(lambda x: x/255, self.to_rgb()))

    def to_hsl(self) -> tuple[float, float, float]:
        r = self.r/255
        g = self.g/255
        b = self.b/255
        cmax = max(r,g,b)
        cmin = min(r,g,b)
        delta = cmax-cmin
        h = 0
        if delta == 0:
            h = 0
        elif cmax == r:
            h = 60 * ( ( (g-b) /delta) % 6 )
        elif cmax == g:
            h = 60 * ( ( (b-r) / delta) + 2 )
        elif cmax == b:
            h = 60 * ( ( (r-g) / delta) + 4 )
        
        l = (cmax + cmin) / 2

        s = 0 if delta == 0 else (delta / (1 - abs(2*l - 1)))
        return (h,s,l)
    
    def to_cmyk(self) -> tuple[float, float, float, float]:
        r = self.r / 255
        g = self.g / 255
        b = self.b / 255
        k = 1 - max(r,g,b)
        c = (1-r-k) / (1-k)
        m = (1-g-k) / (1-k)
        y = (1-b-k) / (1-k)
        return (c,m,y,k)
    
    def to_hex(self) -> str:
        r = hex(self.r)
        g = hex(self.g)
        b = hex(self.b)
        a = hex(int(self.a * 255))
        return r[2:] + g[2:] + b[2:] + a[2:]

    def __repr__(self) -> str:
        return self.to_hex()
    
from kivymd.color_definitions import colors,palette

class ColorDict(Color):
    def __init__(self,colors: dict, is_accent= False) -> None:
        if is_accent == False:
            self.dict = {int(k): Color.from_hex(v) for k,v in colors.items() if not k.startswith("A")}
            default = self.dict[500]
        else:
            self.dict = {int(k[1:]): Color.from_hex(v) for k,v in colors.items() if k.startswith("A")}
            default = self.dict[200]
        super().__init__(default.r, default.g, default.b, default.a)
    def __getitem__(self, key):
        return self.dict[key]

class Colors:
    @classmethod
    @property
    def pink(cls) -> ColorDict:
        return ColorDict(colors["Pink"])
    
    @classmethod
    @property
    def pink_accent(cls) -> ColorDict:
        return ColorDict(colors["Pink"], True)

    @classmethod
    @property
    def red(cls) -> ColorDict:
        return ColorDict(colors["Red"])
    
    @classmethod
    @property
    def red_accent(cls) -> ColorDict:
        return ColorDict(colors["Red"], True)
    
    @classmethod
    @property
    def deep_orange(cls) -> ColorDict:
        return ColorDict(colors["DeepOrange"])
    
    @classmethod
    @property
    def deep_orange_accent(cls) -> ColorDict:
        return ColorDict(colors["DeepOrange"], True)
    
    @classmethod
    @property
    def orange(cls) -> ColorDict:
        return ColorDict(colors["Orange"])
    
    @classmethod
    @property
    def orange_accent(cls) -> ColorDict:
        return ColorDict(colors["Orange"], True)
    
    @classmethod
    @property
    def amber(cls) -> ColorDict:
        return ColorDict(colors["Amber"])
    
    @classmethod
    @property
    def amber_accent(cls) -> ColorDict:
        return ColorDict(colors["Amber"], True)
    
    @classmethod
    @property
    def yellow(cls) -> ColorDict:
        return ColorDict(colors["Yellow"])
    
    @classmethod
    @property
    def yellow_accent(cls) -> ColorDict:
        return ColorDict(colors["Yellow"], True)
    
    @classmethod
    @property
    def lime(cls) -> ColorDict:
        return ColorDict(colors["Lime"])
    
    @classmethod
    @property
    def lime_accent(cls) -> ColorDict:
        return ColorDict(colors["Lime"], True)
    
    @classmethod
    @property
    def light_green(cls) -> ColorDict:
        return ColorDict(colors["LightGreen"])
    
    @classmethod
    @property
    def light_green_accent(cls) -> ColorDict:
        return ColorDict(colors["LightGreen"], True)
    
    @classmethod
    @property
    def green(cls) -> ColorDict:
        return ColorDict(colors["Green"])
    
    @classmethod
    @property
    def green_accent(cls) -> ColorDict:
        return ColorDict(colors["Green"], True)
    
    @classmethod
    @property
    def teal(cls) -> ColorDict:
        return ColorDict(colors["Teal"])
    
    @classmethod
    @property
    def teal_accent(cls) -> ColorDict:
        return ColorDict(colors["Teal"], True)
    
    @classmethod
    @property
    def cyan(cls) -> ColorDict:
        return ColorDict(colors["Cyan"])
    
    @classmethod
    @property
    def cyan_accent(cls) -> ColorDict:
        return ColorDict(colors["Cyan"], True)
    
    @classmethod
    @property
    def light_blue(cls) -> ColorDict:
        return ColorDict(colors["LightBlue"])
    
    @classmethod
    @property
    def light_blue_accent(cls) -> ColorDict:
        return ColorDict(colors["LightBlue"], True)
    
    @classmethod
    @property
    def blue(cls) -> ColorDict:
        return ColorDict(colors["Blue"])
    
    @classmethod
    @property
    def blue_accent(cls) -> ColorDict:
        return ColorDict(colors["Blue"], True)
    
    @classmethod
    @property
    def indigo(cls) -> ColorDict:
        return ColorDict(colors["Indigo"])
    
    @classmethod
    @property
    def indigo_accent(cls) -> ColorDict:
        return ColorDict(colors["Indigo"], True)
    
    @classmethod
    @property
    def purple(cls) -> ColorDict:
        return ColorDict(colors["Purple"])
    
    @classmethod
    @property
    def purple_accent(cls) -> ColorDict:
        return ColorDict(colors["Purple"], True)
    
    @classmethod
    @property
    def deep_purple(cls) -> ColorDict:
        return ColorDict(colors["DeepPurple"])
    
    @classmethod
    @property
    def deep_purple_accent(cls) -> ColorDict:
        return ColorDict(colors["DeepPurple"])
    
    @classmethod
    @property
    def blue_grey(cls) -> ColorDict:
        return ColorDict(colors["BlueGray"])
    
    @classmethod
    @property
    def blue_grey_accent(cls) -> ColorDict:
        return ColorDict(colors["BlueGray"], True)
    
    @classmethod
    @property
    def brown(cls) -> ColorDict:
        return ColorDict(colors["Brown"])
    
    @classmethod
    @property
    def grey(cls) -> ColorDict:
        return ColorDict(colors["Gray"])
    
    @classmethod
    def get_colors(cls) -> list[ColorDict]:
        return [ColorDict(colors[color]) for color in palette]
    
    @classmethod
    def get_accent_colors(cls) -> list[ColorDict]:
        return [ColorDict(colors[color], True) for color in palette]
    
    @classmethod
    def get_colors_with_hue(cls, hue) -> list[Color]:
        return list(map(lambda x: x[hue], cls.get_colors()))
    
    @classmethod
    def get_accent_colors_with_hue(cls, hue) -> list[Color]:
        return list(map(lambda x: x[hue], cls.get_accent_colors()))