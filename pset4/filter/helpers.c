#include "helpers.h"
#include <math.h>


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    float grey;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;

            grey = round((float)(r + g + b) / 3);

            image[i][j].rgbtRed = grey;
            image[i][j].rgbtGreen = grey;
            image[i][j].rgbtBlue = grey;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    float sepr, sepg, sepb;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            int r = image[i][j].rgbtRed;
            int g = image[i][j].rgbtGreen;
            int b = image[i][j].rgbtBlue;

            sepr = round(0.393 * r + 0.769 * g + 0.189 * b);
            sepg = round(0.349 * r + 0.686 * g + 0.168 * b);
            sepb = round(0.272 * r + 0.534 * g + 0.131 * b);

            if (sepr > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(sepr);
            }

            if (sepg > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(sepg);
            }

            if (sepb > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(sepb);
            }

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int h = 0;
    int tmpr, tmpg, tmpb;

    if (width % 2 == 0)
    {
        h = width / 2;


    }
    else
    {
        h = (width - 1) / 2;

    }

    for (int i = 0; i < height; i++)
    {
        int k = 0;

        for(int j = width - 1; j >= h; j--)
        {
            tmpr = image[i][j].rgbtRed;
            tmpg = image[i][j].rgbtGreen;
            tmpb = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][k].rgbtRed;
            image[i][j].rgbtGreen = image[i][k].rgbtGreen;
            image[i][j].rgbtBlue = image[i][k].rgbtBlue;

            image[i][k].rgbtRed = tmpr;
            image[i][k].rgbtGreen = tmpg;
            image[i][k].rgbtBlue = tmpb;

            k++;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    float tmpr, tmpg, tmpb;
    RGBTRIPLE cimage[height][width];

    //copy image
    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            cimage[k][l].rgbtRed = image[k][l].rgbtRed;
            cimage[k][l].rgbtGreen = image[k][l].rgbtGreen;
            cimage[k][l].rgbtBlue = image[k][l].rgbtBlue;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmpr = (float) cimage[i][j].rgbtRed;
            tmpg = (float) cimage[i][j].rgbtGreen;
            tmpb = (float) cimage[i][j].rgbtBlue;

            if (i == 0 && j == 0) //corner top left
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i][j+1].rgbtRed + cimage[i+1][j].rgbtRed + cimage[i+1][j+1].rgbtRed) / 4);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i][j+1].rgbtGreen + cimage[i+1][j].rgbtGreen + cimage[i+1][j+1].rgbtGreen) / 4);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i][j+1].rgbtBlue + cimage[i+1][j].rgbtBlue + cimage[i+1][j+1].rgbtBlue) / 4);
            }
            else if (i == 0 && j == (width - 1)) //corner top right
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i][j-1].rgbtRed + cimage[i+1][j-1].rgbtRed + cimage[i+1][j].rgbtRed) / 4);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i][j-1].rgbtGreen + cimage[i+1][j-1].rgbtGreen + cimage[i+1][j].rgbtGreen) / 4);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i][j-1].rgbtBlue + cimage[i+1][j-1].rgbtBlue + cimage[i+1][j].rgbtBlue) / 4);
            }
            else if (i == (height - 1) && j == 0) //corner down left
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i-1][j].rgbtRed + cimage[i-1][j+1].rgbtRed + cimage[i][j+1].rgbtRed) / 4);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i-1][j].rgbtGreen + cimage[i-1][j+1].rgbtGreen + cimage[i][j+1].rgbtGreen) / 4);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i-1][j].rgbtBlue + cimage[i-1][j+1].rgbtBlue + cimage[i][j+1].rgbtBlue) / 4);
            }
            else if (i == (height - 1) && j == (width - 1)) //corner down right
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i-1][j-1].rgbtRed + cimage[i-1][j].rgbtRed + cimage[i][j-1].rgbtRed) / 4);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i-1][j-1].rgbtGreen + cimage[i-1][j].rgbtGreen + cimage[i][j-1].rgbtGreen) / 4);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i-1][j-1].rgbtBlue + cimage[i-1][j].rgbtBlue + cimage[i][j-1].rgbtBlue) / 4);
            }
            else if (i == 0 && (j > 0 && j < width - 1)) //edge top
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i][j-1].rgbtRed + cimage[i][j+1].rgbtRed + cimage[i+1][j-1].rgbtRed + cimage[i+1][j].rgbtRed + cimage[i+1][j+1].rgbtRed) / 6);
                image[i][j].rgbtGreen = round( (float)(tmpg + cimage[i][j-1].rgbtGreen + cimage[i][j+1].rgbtGreen + cimage[i+1][j-1].rgbtGreen + cimage[i+1][j].rgbtGreen + cimage[i+1][j+1].rgbtGreen) / 6);
                image[i][j].rgbtBlue = round( (float)(tmpb + cimage[i][j-1].rgbtBlue + cimage[i][j+1].rgbtBlue + cimage[i+1][j-1].rgbtBlue + cimage[i+1][j].rgbtBlue + cimage[i+1][j+1].rgbtBlue) / 6);
            }
            else if(j == 0 && (i > 0 && i < height - 1)) //edge left
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i-1][j].rgbtRed + cimage[i+1][j].rgbtRed + cimage[i-1][j+1].rgbtRed + cimage[i][j+1].rgbtRed + cimage[i+1][j+1].rgbtRed) / 6);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i-1][j].rgbtGreen + cimage[i+1][j].rgbtGreen + cimage[i-1][j+1].rgbtGreen + cimage[i][j+1].rgbtGreen + cimage[i+1][j+1].rgbtGreen) / 6);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i-1][j].rgbtBlue + cimage[i+1][j].rgbtBlue + cimage[i-1][j+1].rgbtBlue + cimage[i][j+1].rgbtBlue + cimage[i+1][j+1].rgbtBlue) / 6);
            }
            else if (j == (width - 1) && (i > 0 && i < height - 1)) //edge right
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i-1][j-1].rgbtRed + cimage[i-1][j].rgbtRed + cimage[i][j-1].rgbtRed + cimage[i+1][j-1].rgbtRed + cimage[i+1][j].rgbtRed) / 6);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i-1][j-1].rgbtGreen + cimage[i-1][j].rgbtGreen + cimage[i][j-1].rgbtGreen + cimage[i+1][j-1].rgbtGreen + cimage[i+1][j].rgbtGreen) / 6);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i-1][j-1].rgbtBlue + cimage[i-1][j].rgbtBlue + cimage[i][j-1].rgbtBlue + cimage[i+1][j-1].rgbtBlue + cimage[i+1][j].rgbtBlue) / 6);
            }
            else if (i == (height - 1) && (j > 0 && j < width - 1)) //edge down
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i-1][j-1].rgbtRed + cimage[i-1][j].rgbtRed + cimage[i-1][j+1].rgbtRed + cimage[i][j-1].rgbtRed + cimage[i][j+1].rgbtRed) / 6);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i-1][j-1].rgbtGreen + cimage[i-1][j].rgbtGreen + cimage[i-1][j+1].rgbtGreen + cimage[i][j-1].rgbtGreen + cimage[i][j+1].rgbtGreen) / 6);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i-1][j-1].rgbtBlue + cimage[i-1][j].rgbtBlue + cimage[i-1][j+1].rgbtBlue + cimage[i][j-1].rgbtBlue + cimage[i][j+1].rgbtBlue) / 6);
            }
            else //rest inside
            {
                image[i][j].rgbtRed = round((float)(tmpr + cimage[i-1][j-1].rgbtRed + cimage[i-1][j].rgbtRed + cimage[i-1][j+1].rgbtRed + cimage[i][j-1].rgbtRed + cimage[i][j+1].rgbtRed + cimage[i+1][j-1].rgbtRed + cimage[i+1][j].rgbtRed + cimage[i+1][j+1].rgbtRed) / 9);
                image[i][j].rgbtGreen = round((float)(tmpg + cimage[i-1][j-1].rgbtGreen + cimage[i-1][j].rgbtGreen + cimage[i-1][j+1].rgbtGreen + cimage[i][j-1].rgbtGreen + cimage[i][j+1].rgbtGreen + cimage[i+1][j-1].rgbtGreen + cimage[i+1][j].rgbtGreen + cimage[i+1][j+1].rgbtGreen) / 9);
                image[i][j].rgbtBlue = round((float)(tmpb + cimage[i-1][j-1].rgbtBlue + cimage[i-1][j].rgbtBlue + cimage[i-1][j+1].rgbtBlue + cimage[i][j-1].rgbtBlue + cimage[i][j+1].rgbtBlue + cimage[i+1][j-1].rgbtBlue + cimage[i+1][j].rgbtBlue + cimage[i+1][j+1].rgbtBlue) / 9);
            }
        }
    }
    return;
}
