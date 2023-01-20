import random

import cv2 as cv


class Particle:
    def __init__(self, location):
        self.x_location = int(location[0])
        self.y_location = int(location[1])
        self.color = [random.randrange(0, 50), random.randrange(0, 50), random.randrange(0, 256)]

    def update(self):
        self.x_location += random.randrange(-2, 3)
        self.y_location += random.randrange(-2, 3)

    def draw_on_image(self, photo):
        cv.circle(photo, [self.x_location, self.y_location], 3, self.color, -1)


def create_particles(particles_list, amount, location):
    for i in range(amount):
        particles_list.append(Particle(location))
    return particles_list


def display_all_particles(particles_list, image):
    for particle in particles_list:
        particle.draw_on_image(image)
        particle.update()


def delete_all_particles(particles_list):
    for particle in particles_list:
        del particle
    return []
