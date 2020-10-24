from .component import Component

class Chatbot:
    
    def __init__(self, components):
        self.components = components
        for i in range(len(components)-1):
            components[i].connect(components[i+1])
        components[-1].connect(components[0])

    def step(self, timesteps=1):
        for _ in range(timesteps):
            for c in self.components:
                c.run()


