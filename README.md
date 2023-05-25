# GIFmaker

<p align="center">
<img src="demo.png.gif" width=50% height=50% 
class="center">
</p>

PIL/cv2 are common libs for computer vision and support creating GIFs. 
Here we demo a simple process to implement some typical demands for creating a GIF. Now you can manipulate the imgs and logic on your own!

We will publish more functions like output a given length or size.

## Start!
If you are experienced in deep learning, you may not have to build this because most packages are common in deep learning.

```
git clone https://github.com/kytimmylai/GIFmaker.git
conda create --name GIFmaker python=3.9
conda activate GIFmaker
cd GIFmaker
pip install -r requirements.txt
```

Now you can create the GIF by
```
python gifmaker.py --n demo.png
```