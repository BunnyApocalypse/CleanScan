import Cleaning
import Gutter

k, finalImg = gutter(img1)
crop1, crop2 = makeCrops(mask, finalImg)
lines, lines2 = cropLines(crop1, crop2)
verticaLines, verticaLines2 = verticalSort(lines, lines2, crop1, crop2)
angle, secondAngle = minMaxLines(verticaLines, verticaLines2)
rotateCrops(crop1, crop2, angle, secondAngle)


