# What is StormViewer?

This is a little app written in Python that calculates the critical storm for a TUFLOW ensemble simulation as per the ARR2019 guidelines (refer to ARR2019, book 2, chapter 5). This tool processes flow volumes generated at PO Lines in order to determine critical flow configurations (these files are named in the pattern \*_PO.csv and are generated by TUFLOW.) 

The outputs of the tool are:

1. A results file ("StormViewer_results.csv") that displays the critical duration and temporal pattern for each event and PO line in your model; and
2. A box plot for each storm event and PO Line processed.

# How do I use it?

Ensure that your TUFLOW models are set up to generate results named according to standard naming conventions discussed below. Then, simply choose the folder containing the PO line CSV results files as the input directory and StormViewier will calculate the critical storms for each PO line. If you choose to plot your storms, you can navigate plots by clicking the storm you wish to visualize in the results table. 

### A note on filename conventions

StormViewier parses the filenames of your \*_PO.csv files to interpret storm event / duration / temporal pattern. As such, your csv files should be named so that your storm event, duration and temporal pattern are separated by underscores. This tool looks for the following (NOT case sensitive):

1. Storm Event is the text between the first and second underscores in your filename.
2. Duration is the number(s) preceding "m_" in your filename
3. Temporal Pattern is the number(s) after the string "tp" in your filename.

As such, a po line CSV result named "Example-Catchment_0.5EY_360m_tp07_no-blockages_001_PO.csv" would be understood to be Event 0.5EY, Duration 360 minutes and Temporal Pattern 7.

