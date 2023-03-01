# Layout Walkthrough for OMAX/PROTOMAX Layout
This is a guide for taking a file with vectors (AutoCAD .dwg or .dxf, vector graphic .svg, or Illustrator .ai) and creating toolpaths and instruction sets for the waterjet using PROTOMAX Layout to then be ran on the waterjet. You'll need the vector pathing file, as well as PROTOMAX Layout included in [this free software package](https://www.omax.com/libraries/omax/download/) from OMAX. Unarchive the downloaded file, then run the installer to get Layout, then continue. 

## Deciphering Layout's Interface
Layout's interface is a little more obfuscated than most modern CAD softwares'. However, if you've used AutoCAD, it will feel similar. The main tools are on your left and right side, as well as bottom, toolbars, with each option having extras when right-clicked. 

![image](https://user-images.githubusercontent.com/63514508/211653132-b2d55a3d-44c6-4816-a729-41f78d72dd2c.png)

The left toolbar is mostly creating and editing paths and vectors, the bottom is viewing tools and configuration settings (like zoom, dimensions, and background color), and the right has functions for finishing and exporting. 


## Layout
1. Open Layout, then go to `File` -> `Import from other CAD`. After finding and selecting your vector file, hit `Open` to import it. The following window will appear.

![image](https://user-images.githubusercontent.com/63514508/211651199-d8444f81-2103-46dd-b2a1-b0e7245fdc9a.png)

The main display shows a preview of what your file will look like when imported. This may not perfectly match what you imported, and you can use the `Spline Curve Conversion Tolerance` and `Ellipse Curve Conversion Tolerance` sliders on the left to adjust it. Additionally, there are some viewing tools (pan, zoom, etc) near the bottom right of the display panel. Once you have the sliders adjusted the way you want, you can hit `Ok` in the bottom left. This will finish the importing process.

2. Once you have your job imported to PROTOMAX, first check your scale. The `Measurement` option in the bottom row can measure lengths between two points, in the document's units. You can change the documents units by going to `Config` in the bottom row, and then selecting your preferred units in the dropdown, as shown below. 

![image](https://user-images.githubusercontent.com/63514508/212764168-d6e244c1-a848-4512-a66f-d509338bbf6e.png)

You can also rescale elements by using the `Size` option in the upper left. Then you can set the X and Y dimensions of the selected elements. By default, the aspect ratio is set, meaning the proportions of the elements will be maintained by rescaling. This can be changed by selecting the `Stretch - Arcs become oval` option. 

3. You can select extra pieces that got imported by using the `Select` tool, and then pressing the delete key with them highlighted. Here I am using the `Window` select tool. 

![image](https://user-images.githubusercontent.com/63514508/211654491-3efa5e60-af86-492c-9ba8-d3d1bcd1cdd4.png)

![image](https://user-images.githubusercontent.com/63514508/211654582-69182b5a-f4f3-4dc7-bbb2-41172ac2ce8a.png)

4. Now that you only have the paths you want to use, we can set the quality, or the operation that will be taken with each path. In order to do this, select the paths you want for a specfic operation, then right-click the `Quality` option on the bottom row, finding `Selected` to set the quality for the paths you have selected. 

![image](https://user-images.githubusercontent.com/63514508/211655869-1076c893-978d-42ab-964f-d15164919738.png)

This will bring up a window with the different quality options. 

![image](https://user-images.githubusercontent.com/63514508/211655979-1e4fe5b5-8bb8-4921-8180-1f66ddadb8ee.png)

 * T - Heads-Down Traverse: Moving the head without using the jet or abrasive, or raising the head, as opposed to Heads-Up Traverse

 * 1-5 - Progressively finer Cuts: Using the jet and abrasive to cut through material. The finer the cut you make, the slower the cut and the more garnet it uses. 

 * e - Etch (With abrasive): Engraving on material using the jet and abrasive. 

 * Lead i/o - Lead In/Lead Out: Leading into or out of a cut. When making a cut, starting it has a much higher kerf, or amount of material taken out, than it does while making the main cut. The solution to this, so as to not have weird wide parts of cuts, is to lead in on the offcut side of the material. This will be done automatically by default, but this option is a manual way to do it.

For most jobs, if you don't need really small tolerances, 3 will do fine for cutting. 

5. Next is tabbing. Tabs are indents that connects cut pieces so that they don't fall into the tank of the waterjet while machining. Generally, you want your tabs to be on the offcut side of your material, so that you don't have chunks taken out from your good pieces. You can start tabbing by pressing Control + T, or right-clicking `Lead i/o` on the right hand side and selecting `Create Tab`. Clicking near one of your paths will now create a tab on that path, leading out to the side you clicked on. 

![image](https://user-images.githubusercontent.com/63514508/211659149-10843ef4-ebb5-41ac-9d3c-7a07fd359a5b.png)

Tabs are removed by sawing through them with a hand saw, or twisting them off similar to sprues on injection-molded model kits. So, you generally want to put them on a long, flat side near one edge so that you have room to get in and cut through them. 

![image](https://user-images.githubusercontent.com/63514508/211660932-fc35369f-78c9-40dd-8f96-e4043e01fb88.png)

6. Once you have your tabs done and your operation types selected, what's left is finishing, pathing and postprocessing. Find the `Clean` option on the right hand side, and then hit start. This will clean up unnecessary paths and dots.

![image](https://user-images.githubusercontent.com/63514508/211661456-bb8fe99e-b498-4dca-b110-a7b16db0d42f.png)

7. Next, pathing. On the left-hand side, right-click `Autopath` and find `Advanced and Configure`. From here, you can preview the toolpaths that will be generated and manipulate them to some degree. This is the easiest part to mess and have it impact your piece, so be careful and use the preview. 

![image](https://user-images.githubusercontent.com/63514508/211663851-d8a481ad-9434-484e-8260-69544f51931e.png)

Notice here how the leads (brown) are on the good piece, and will damage it. This can be fixed by going out of the Autopathing tool and drawing a box around our piece. This tells the autopather that the piece we want is the piece we want to keep, and it will treat it accordingly. The paths for the box can then be deleted after the path is generated.

![image](https://user-images.githubusercontent.com/63514508/211664717-39db6b7e-84c7-451e-a4aa-808236a055d0.png)

After deleting the box: 

![image](https://user-images.githubusercontent.com/63514508/211664921-06ac2270-c655-46bd-aabc-5abc880e2360.png)

8. Finally, all that needs done is post-processing. Find the `Post` option on the right hand side and select it. It will ask you to select a starting point, which should be the bottom-left path as shown below. 

![image](https://user-images.githubusercontent.com/63514508/211665177-ead13650-46e5-41bd-b51b-85c922156b4d.png)

It may show a screen similar to the one below, with some paths in yellow. Here it is asking you to choose which direction to go, clicking on a yellow path will choose it. 

![image](https://user-images.githubusercontent.com/63514508/211665324-a566e130-0118-44bd-b415-e014b32e77d7.png)

It will then open a dialogue box to save your paths, and you're done! 
