<div align="center">
  
<h1>🎯Valorant Triggerbot🎯</h1>

This project was developed for Windows OS only.
A project by [**Thegladster**](https://github.com/Thegladster).

<div align="left">
<details open>
  
<summary><b>Prerequisites</b></summary>

<h4>1.</h4>
Make sure enemy color setting is set to deuteranopia.

<h4>2.</h4>

For faster screen recording, it is **highly recommended** (but not necessary) to set all settings to low.

<h4>3.</h4>
Make sure you keybind the 'shoot' button to the key '0'.

</details>
<details>
  
<summary><b>Usage</b></summary>

<h4>1.</h4>
Download ZIP, extract all, and run following command in Command Prompt (no changes need to be made as long as the folder is saved in Downloads):

```bash
cd C:\Users\%username%\Downloads\val-triggerbot-main\val-triggerbot-main
pip install -r requirements.txt
python triggerbot.py
```

<h4>2.</h4>
For future uses after initialization, run the following command:

```bash
cd C:\Users\%username%\Downloads\val-triggerbot-main\val-triggerbot-main
python triggerbot.py
```

</details>
<details>

<summary><b>Menu Selection</b></summary>

<h4>1.</h4>
Upon running, you will have to select the gun you are going to use with the bot in order for the bot to spray depending on accuracy.

Simply type the gun in **all lowercase** with no extra spaces.

> Note that just for the Operator, you can just type `op`.

2. If the gun changes later on (which it most likely will), or you would like to exit the program, open command prompt and type `alt + p`. If you would like to exit, simply type `exit`.

</details>
<details>

<summary><b>FPS Troubleshooting</b></summary>

<h4></h4>

The reported FPS should be at or around the game's client FPS, which should consequently be at or around your monitor's [**refresh rate.**](https://support.microsoft.com/en-us/windows/change-the-refresh-rate-on-your-monitor-in-windows-c8ea729e-0678-015c-c415-f806f04aae5a)

If your game FPS is significantly higher than the reported FPS from the triggerbot, there can be many different possibilities:

<h4>1. VALORANT is utilizing too many resources</h4>
If your PC is barely running VALORANT at 120 FPS, then it would be nearly impossible for it to run the triggerbot at the same time. 


To counter this, **set all settings to 'Low' and change the max FPS that VALORANT can run on** to fix this issue. Note that this triggerbot may not work for low-end computers. You can see the bot's CPU usage in 
[**Task Manager.**](https://www.tomsguide.com/how-to/how-to-open-task-manager-on-windows)

Note that this triggerbot DOES have ~240Hz capabilities, it is just up to the computer that runs it whether or not that mark can be hit.

<h4>2. Inaccurate reporting results</h4>
Screenshots are only taken when a **change in frame is reported.** This means that the more you are still in-game (not moving, shooting, etc), the FPS will drop. This doesn't indicate a problem with your computer, just an inaccuracy on the triggerbot's end.

Moreover, shooting opponents will also lower FPS because frames are not recorded when you are shooting. This means that if you are in the range and are constantly shooting bots, the report FPS will drop. Once again, the actual FPS does not drop, but less frames are taken per second because you are constantly shooting.

To know when your results are simply inaccurate or if it is a problem with your computer, hop into a game and just move the camera around sporadically for 30 seconds. Do not stop the camera's movement until you press `alt + p`, and see if the reported FPS matches with your game FPS.
