import re, base64

inputfolder_name = "input"
outputfolder_name = "output"

basefile_name = "base.html"
bodyfile_name = "body.md"

outputfile_name = "index.html"

try:
    basefile = open(inputfolder_name + "/" + basefile_name, "r")
except FileNotFoundError:
    print("Base file not found at specified path.")
    exit(1)

outputfile = open(outputfolder_name + "/" + outputfile_name, "w")


for line in basefile:
    # Look for a line with the string "{{path/to/filename.md}}" in it.
    if re.search("\\{\\{(.*)\\.md\\}\\}", line) != None:
        try: 
            # group() gets the result from the re.Match object as a string.
            # [2:-2] removes the leading and trailing "{{}}"
            bodyfile_name = inputfolder_name + "/" + re.search("\\{\\{(.*)\\.md\\}\\}", line).group()[2:-2]
            bodyfile = open(bodyfile_name, "r")

            codeBlockStarted = False

            for bodyline in bodyfile:
                
                # Line with an internal comment: discard.
                if bodyline.startswith("// "):
                    continue

                # Start/end of a block of code.
                elif bodyline.startswith("```"):
                    
                    if codeBlockStarted == False:
                        outputfile.write("<div class = \"code\">")
                        codeBlockStarted = True
                    else:
                        outputfile.write("</div>\n")
                        codeBlockStarted = False
                
                elif codeBlockStarted == False:
                    # Header line found.
                    if bodyline[0] == "#" and len(bodyline) - len(bodyline.lstrip('#')) <= 6:
                        headertype = str(len(bodyline) - len(bodyline.lstrip('#')))
                        bodyline = "<h" + headertype + ">" + bodyline[:-1] + "</h" + headertype + ">\n"
                    # Code line found; replace `` with <span> tags.
                    # Regex groups are wonderful, I think
                    code_re = "`(?P<code>.*)`"
                    if re.search(code_re, bodyline) != None:
                        bodyline = re.sub(code_re, "<span class=\"code\">\g<code></span>", bodyline)

                    
                    dontcapture_re = "[^\*_\\n]"
                    
                    bolditalics_re = "(\*\*\*|___)(?! )(?P<bolditalics>" + dontcapture_re + "+?)(?! )(\*\*\*|___)"
                    if re.search(bolditalics_re, bodyline) != None:
                        bodyline = re.sub(bolditalics_re, "<strong><em>\g<bolditalics></em></strong>", bodyline)
                    # Bold text
                    bold_re = "(\*\*|__)(?! )(?P<bold>" + dontcapture_re + "+?)(?! )(\*\*|__)"
                    if re.search(bold_re, bodyline) != None:
                        bodyline = re.sub(bold_re, "<strong>\g<bold></strong>", bodyline)
                    
                    # Italics
                    italics_re = "(?<!\\\\)(?<!\*)(?<!_)(\*|_)(?! )(?P<italics>" + dontcapture_re + "+?)(?! )(\*|_)(?!\\\\|\*|_)"
                    if re.search(italics_re, bodyline) != None:
                        bodyline = re.sub(italics_re, "<em>\g<italics></em>", bodyline)
                    
                    links_re = "(?<!!)\[(?P<linktext>.*)\]\((?P<href>.*)\)"
                    if re.search(links_re, bodyline) != None:
                        bodyline = re.sub(links_re, "<a href='\g<href>'>\g<linktext></a>", bodyline)

                    images_re = "!\[(?P<imagetext>.*)\]\((?P<imgsrc>.*)\)"
                    if re.search(images_re, bodyline) != None:


                        # Encode image to base64
                        with open(inputfolder_name + "/" + re.search(images_re, bodyline).group(2), "rb") as image_file: 
                            encoded_string = "data:image/svg+xml;base64," + base64.b64encode(image_file.read()).decode("utf-8")

                            bodyline = re.sub(images_re, "<img src=" + encoded_string + " alt='\g<imagetext>' title='\g<imagetext>'/>", bodyline)
                        

                    # Write line to output
                    outputfile.write(bodyline)

                # Part of code block
                else:
                    outputfile.write(bodyline)

                
            bodyfile.close()
            
        except FileNotFoundError:
            print("Body file not found at specified path.")   
            exit(1)
        
    else:
        outputfile.write(line)

basefile.close()
outputfile.close()

