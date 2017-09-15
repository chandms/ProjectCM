from xml.etree import ElementTree as ET
import csv

tree = ET.parse('reed.xml')
root = tree.getroot()

reed_file= open('reedfile.csv','w')

csvwriter = csv.writer(reed_file)

rh =[]

count=0

for member in root:
    course =[]
    time_list =[]
    place_list =[]
    if count==0:
        reg_num=member.find('reg_num').tag
        rh.append(reg_num)
        subj=member.find('subj').tag
        rh.append(subj)
        crse=member.find('crse').tag
        rh.append(crse)
        sect=member.find('sect').tag
        rh.append(sect)
        title=member.find('title').tag
        rh.append(title)
        units=member.find('units').tag
        rh.append(units)
        instructor=member.find('instructor').tag
        rh.append(instructor)
        days=member.find('days').tag
        rh.append(days)
        time=member[8].tag
        rh.append(time)
        place=member[9].tag
        rh.append(place)
        csvwriter.writerow(rh)
        count=count+1


    reg_num= member.find('reg_num').text
    course.append(reg_num)
    subj=member.find('subj').text
    course.append(subj)
    crse=member.find('crse').text
    course.append(crse)
    sect=member.find('sect').text
    course.append(sect)
    title=member.find('title').text
    course.append(title)
    units=member.find('units').text
    course.append(units)
    instructor=member.find('instructor').text
    course.append(instructor)
    days=member.find('days').text
    course.append(days)
    time=member[8][0].text
    time_list.append(time)
    end_time=member[8][1].text
    time_list.append(end_time)
    course.append(time_list)
    place=member[9][0].text
    place_list.append(place)
    room=member[9][1].text
    place_list.append(room)
    course.append(place_list)
    csvwriter.writerow(course)
reed_file.close()
        
