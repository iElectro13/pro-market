import cv2 as cv
import numpy as np

prueba = "Highest Price: 1,500 gold"
separado = prueba.split()
separado = separado[-2]
separado = int(separado.replace(",", ""))