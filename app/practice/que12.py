import random
import string

class TinyURL:

    def __init__(self):
        self.url_to_code={}
        self.code_to_url={}

    def generate_code(self):
        characters=string.ascii_letters+string.digits
        while True:
            code=''.join(random.choice(characters) for _ in range(6))
            if code not in self.code_to_url:
                return code
            
    def shorten(self,url):
        if url in self.url_to_code:
            return self.url_to_code[url]

        code=self.generate_code()
        self.url_to_code[url]=code
        self.code_to_url[code]=url

        return code

    def expand(self,code):
        return self.code_to_url.get(code,"Invalid code")





tiny = TinyURL()

code1 = tiny.shorten("https://www.gle.com")
code2=tiny.shorten("https://www.google.com")

print("Short Code:", code1)
print("Short Code:", code2)

print("Original URL:", tiny.expand(code1))
print("Original URL:", tiny.expand(code2))

print("Same URL:", tiny.shorten("https://www.google.com"))
