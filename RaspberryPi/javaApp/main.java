import java.awt.*;
import java.awt.image.BufferedImage;

import java.io.*;

import javax.imageio.ImageIO;
import javax.swing.JFrame;

class Main {
  public static void main(String[] args) {
    BufferedImage image = null;
    File inputImage = null;

    int width = 0, height = 0;

    try {
      inputImage = new File("thermal_image.jpeg");

      image = ImageIO.read(inputImage);
      width = image.getWidth();
      height = image.getHeight();

      for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
          int color = image.getRGB(j, i);
          int r = (color >> 24) & 0xff;
          int g = (color >> 16) & 0xff;
          int b = (color >> 8) & 0xff;
          System.out.println("Pixel (" + j + ", " + i + ") color: " + r + " " + g + " " + b);
        }
      }
    }
    catch (Exception e) {
      System.out.println("Exception " + e);
    }
  }
}
