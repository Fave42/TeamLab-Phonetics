#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Fabian Fey
# @Author: Matthias Wilke

import sqlite3
from sqlite3 import Error
import codecs
import csv
import re
import sys
import unicodedata
import string
import os

reload(sys)  
sys.setdefaultencoding('utf8')

titleDict = {}
data = []

ASCII_REPLACEMENTS = {
    'À': 'A',
    'Á': 'A',
    'Â': 'A',
    'Ã': 'A',
    'Ä': 'A',
    'Å': 'A',
    'Æ': 'AE',
    'Ç': 'C',
    'È': 'E',
    'É': 'E',
    'Ê': 'E',
    'Ë': 'E',
    'Ì': 'I',
    'Í': 'I',
    'Î': 'I',
    'Ï': 'I',
    'Ð': 'D',
    'Ñ': 'N',
    'Ò': 'O',
    'Ó': 'O',
    'Ô': 'O',
    'Õ': 'O',
    'Ö': 'O',
    'Ø': 'O',
    'Ù': 'U',
    'Ú': 'U',
    'Û': 'U',
    'Ü': 'U',
    'Ý': 'Y',
    'Þ': 'Th',
    'ß': 'ss',
    'à': 'a',
    'á': 'a',
    'â': 'a',
    'ã': 'a',
    'ä': 'a',
    'å': 'a',
    'æ': 'ae',
    'ç': 'c',
    'è': 'e',
    'é': 'e',
    'ê': 'e',
    'ë': 'e',
    'ì': 'i',
    'í': 'i',
    'î': 'i',
    'ï': 'i',
    'ð': 'd',
    'ñ': 'n',
    'ò': 'o',
    'ó': 'o',
    'ô': 'o',
    'õ': 'o',
    'ö': 'o',
    'ø': 'o',
    'ù': 'u',
    'ú': 'u',
    'û': 'u',
    'ü': 'u',
    'ý': 'y',
    'þ': 'th',
    'ÿ': 'y',
    'Ł': 'L',
    'ł': 'l',
    'Ń': 'N',
    'ń': 'n',
    'Ņ': 'N',
    'ņ': 'n',
    'Ň': 'N',
    'ň': 'n',
    'Ŋ': 'ng',
    'ŋ': 'NG',
    'Ō': 'O',
    'ō': 'o',
    'Ŏ': 'O',
    'ŏ': 'o',
    'Ő': 'O',
    'ő': 'o',
    'Œ': 'OE',
    'œ': 'oe',
    'Ŕ': 'R',
    'ŕ': 'r',
    'Ŗ': 'R',
    'ŗ': 'r',
    'Ř': 'R',
    'ř': 'r',
    'Ś': 'S',
    'ś': 's',
    'Ŝ': 'S',
    'ŝ': 's',
    'Ş': 'S',
    'ş': 's',
    'Š': 'S',
    'š': 's',
    'Ţ': 'T',
    'ţ': 't',
    'Ť': 'T',
    'ť': 't',
    'Ŧ': 'T',
    'ŧ': 't',
    'Ũ': 'U',
    'ũ': 'u',
    'Ū': 'U',
    'ū': 'u',
    'Ŭ': 'U',
    'ŭ': 'u',
    'Ů': 'U',
    'ů': 'u',
    'Ű': 'U',
    'ű': 'u',
    'Ŵ': 'W',
    'ŵ': 'w',
    'Ŷ': 'Y',
    'ŷ': 'y',
    'Ÿ': 'Y',
    'Ź': 'Z',
    'ź': 'z',
    'Ż': 'Z',
    'ż': 'z',
    'Ž': 'Z',
    'ž': 'z',
    'ſ': 's',
    'Α': 'A',
    'Β': 'B',
    'Γ': 'G',
    'Δ': 'D',
    'Ε': 'E',
    'Ζ': 'Z',
    'Η': 'E',
    'Θ': 'Th',
    'Ι': 'I',
    'Κ': 'K',
    'Λ': 'L',
    'Μ': 'M',
    'Ν': 'N',
    'Ξ': 'Ks',
    'Ο': 'O',
    'Π': 'P',
    'Ρ': 'R',
    'Σ': 'S',
    'Τ': 'T',
    'Υ': 'U',
    'Φ': 'Ph',
    'Χ': 'Kh',
    'Ψ': 'Ps',
    'Ω': 'O',
    'α': 'a',
    'β': 'b',
    'γ': 'g',
    'δ': 'd',
    'ε': 'e',
    'ζ': 'z',
    'η': 'e',
    'θ': 'th',
    'ι': 'i',
    'κ': 'k',
    'λ': 'l',
    'μ': 'm',
    'ν': 'n',
    'ξ': 'x',
    'ο': 'o',
    'π': 'p',
    'ρ': 'r',
    'ς': 's',
    'σ': 's',
    'τ': 't',
    'υ': 'u',
    'φ': 'ph',
    'χ': 'kh',
    'ψ': 'ps',
    'ω': 'o',
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'I',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'Kh',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shch',
    'Ъ': "'",
    'Ы': 'Y',
    'Ь': "'",
    'Э': 'E',
    'Ю': 'Iu',
    'Я': 'Ia',
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': "'",
    'ы': 'y',
    'ь': "'",
    'э': 'e',
    'ю': 'iu',
    'я': 'ia',
    # 'ᴀ': '',
    # 'ᴁ': '',
    # 'ᴂ': '',
    # 'ᴃ': '',
    # 'ᴄ': '',
    # 'ᴅ': '',
    # 'ᴆ': '',
    # 'ᴇ': '',
    # 'ᴈ': '',
    # 'ᴉ': '',
    # 'ᴊ': '',
    # 'ᴋ': '',
    # 'ᴌ': '',
    # 'ᴍ': '',
    # 'ᴎ': '',
    # 'ᴏ': '',
    # 'ᴐ': '',
    # 'ᴑ': '',
    # 'ᴒ': '',
    # 'ᴓ': '',
    # 'ᴔ': '',
    # 'ᴕ': '',
    # 'ᴖ': '',
    # 'ᴗ': '',
    # 'ᴘ': '',
    # 'ᴙ': '',
    # 'ᴚ': '',
    # 'ᴛ': '',
    # 'ᴜ': '',
    # 'ᴝ': '',
    # 'ᴞ': '',
    # 'ᴟ': '',
    # 'ᴠ': '',
    # 'ᴡ': '',
    # 'ᴢ': '',
    # 'ᴣ': '',
    # 'ᴤ': '',
    # 'ᴥ': '',
    'ᴦ': 'G',
    'ᴧ': 'L',
    'ᴨ': 'P',
    'ᴩ': 'R',
    'ᴪ': 'PS',
    'ẞ': 'Ss',
    'Ỳ': 'Y',
    'ỳ': 'y',
    'Ỵ': 'Y',
    'ỵ': 'y',
    'Ỹ': 'Y',
    'ỹ': 'y',
}

def isascii(text):
    """Test if ``text`` contains only ASCII characters.
    :param text: text to test for ASCII-ness
    :type text: ``unicode``
    :returns: ``True`` if ``text`` contains only ASCII characters
    :rtype: ``Boolean``
    """
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

def fold_to_ascii(text):
        """Convert non-ASCII characters to closest ASCII equivalent.
        .. versionadded:: 1.3
        .. note:: This only works for a subset of European languages.
        :param text: text to convert
        :type text: ``unicode``
        :returns: text containing only ASCII characters
        :rtype: ``unicode``
        """
        if isascii(text):
            return text
        text = ''.join([ASCII_REPLACEMENTS.get(c, c) for c in text])
        return unicode(unicodedata.normalize('NFKD',unicode(text)).encode('ascii', 'ignore'))


def createTitleDict():
    print("Creating titleDict...")
    with codecs.open('title.basics.tsv', 'r', encoding='utf8') as titleFile:
        next(titleFile)
        for line in titleFile:
            # tconst    titleType    primaryTitle    originalTitle    isAdult    startYear    endYear    runtimeMinutes    genres
            
            line = line.lower()
            #represent empty values as -1
            line = line.replace("\\n", "-1")
            line = fold_to_ascii(line)
            lineSplit = line.split("\t")
            #don't add adult films, films made before 1960 or films with a runtime of less than 10 minutes to our data
            if (int(lineSplit[4]) == 1 or int(lineSplit[5]) < 1980 or int(lineSplit[7]) < 10):
                continue
            #set title id as key for the dictionary
            tconst = lineSplit[0]
            #create a version of the line where the tconst, the isAdult boolean, and the end year are removed
            lineShort = lineSplit
            lineShort.pop(0)  # tconst
            lineShort.pop(2)  # originalTitle
            lineShort.pop(2)  # isAdult
            lineShort.pop(3)  # endYear

            #add the genres as one string to our line
            lineShort.append(lineShort.pop(4).replace("\n",""))
            #save all the movie info as one string into our dictionary with tconst as a key
            # primaryTitle : titleType, startyear (genres, runtimeMinutes)
            if lineShort[2] == "-1" or lineShort[4] == "-1" or lineShort[3] == "-1":
                continue
            lineString = "{0} : {1}, {2} ({3}, {4} minutes)".format(lineShort[1],lineShort[0],lineShort[2],lineShort[4],lineShort[3])
            titleDict[tconst] = lineString
                
    print("\tCreated titleDict...")


def createData():
    print("Creating Data...")
    with codecs.open('name.basics.tsv', 'r',encoding='utf8') as actorFile:
        next(actorFile)
        dataFileName = 'persons.tsv'
        try:
            os.remove(dataFileName)
        except OSError:
            pass
        
        dataFile = codecs.open(dataFileName, 'w',encoding='utf8')
        for line in actorFile:
            # nconst  actorName     birthYear       deathYear       professions       knownForTitles
            
            line = line.lower()
            #represent empty values as -1
            line = line.replace("\\n", "-1")
            line = fold_to_ascii(line)
            #delete single quotation marks around stage names
            line = (re.sub("'.*?'","",line)).replace("  "," ")
            #create a list from tab-separated contents
            lineSplit = line.split("\t")
            if lineSplit[2] == "-1":
                continue
            #exclude the numerical identifier
            # lineSplit.pop(0)  # Fabian
            #create a list for the comma-separated attributes of each movie
            titleList = lineSplit.pop(5).replace('\n', '').split(',')
            #append the professions
            professionString = lineSplit.pop(4).replace("_"," ").replace(",",", ")
            lineSplit.append(professionString)
            #ignore actors with less than 2 movies
            if len(titleList) < 2:
                continue
            #if one movie is not in the preprocessed movie list, don't add it
            titleString = ""
            for title in titleList:
                if title in titleDict:
                    titleString += ("|{0}| ".format(titleDict[title].replace("\n", "").replace("\"", "'")))
                else:
                    lineSplit = []
            lineSplit.append(titleString)
            #prevent entries with missing data from being added
            if(len(lineSplit) <= 3):
                continue
            data.append(lineSplit)
            #write to persons.tsv
            actorString = "\t".join(lineSplit)+"\n"
            dataFile.write(actorString)
            #print (actorString)
        dataFile.close()
    print("\tCreated Data...")


def writeToDatabase(db_file):
    try:
        os.remove(db_file)
    except OSError:
        pass
    print("Writing to Database...")
    with codecs.open('persons.tsv', 'r',encoding='utf8') as dataFile:
        # create a database connection to a SQLite database
        tableName = "IMDB"
    
        columns = ["id",
        "name",
        "birthyear", 
        "deathyear", 
        "professions", 
        "movieinfo"
        ]
    
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
    
        #~ attributes = "(" + (", ".join(columns)) + ")"
        numAttributes = ",".join(["?"] * len(columns))
    
    
        try:
            #create our table, always clear existing ones with the same name. Init column names.
            c.execute("DROP TABLE IF EXISTS {tn}".format(tn = tableName))
            c.execute("CREATE TABLE {tn} ({nc})".format(tn = tableName, nc = ','.join(columns)))
            #add the rest of the columns to the table
        except Error as e:
            print(e)
    
        #loop over all actors to fill our database
        for line in dataFile:
            actor = line.replace("\n","").split("\t")
            c.execute("insert into {tn} values ({na})".format(tn=tableName,na=numAttributes), actor)
        conn.commit()
        conn.close()
        print("\tWrote the Database...")


def testDataBase(db_file):
    # create a database connection to a SQLite database
    tableName = "IMDB"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    c.execute("SELECT * from {tn}".format(tn=tableName))
    data = c.fetchall()
    for actor in data:
        print (actor)
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # createTitleDict()
    # createData()
    # writeToDatabase("imdb_chopped.db")
    testDataBase("imdb_chopped.db")
