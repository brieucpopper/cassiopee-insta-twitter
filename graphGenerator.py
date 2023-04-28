#This python program generates different graphs for
#Different Newspaper's social media performance on Instagram and Twitter

#imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


#constants
newspapersTwitter=['Le_Figaro','ParisMatch','Valeurs','GALAfr','marieclaire','ELLEfrance','OnzeMondial','libe','Psychologies_','Santeplusmag','PointDeVueMag','LesEchos','Madamefigaro','publicsenat','lemondefr','voici','femmeactuelle','EnduroMagazine1','midi_olympique','sofoot','AutoPlusMag','humanite_fr','purepeople','lequipe']
subsTwitter=[3693892, 1283885, 397001, 70097, 2186301, 545664, 81473, 3506288, 65536, 3388, 5889, 1393546, 1026296, 416872, 10613782, 249687, 17101, 3396, 58554, 380098, 47739, 396309, 63834, 6526327]



def statsOnDatabase(data):
    #gives some basic information about the database which is a pandas df
    print("The shape of the database is: ",data.shape)
    print("The columns of the database are: ",data.columns)

    #print out randomly a sample of 5 rows with each column printed separately
    print("A sample of 5 rows of the database is: ")
    print(data.sample(5))

    #for a specific sample go more in details
    sample=data.head(1)
    keys=sample.keys()

    for key in keys:
        print(key,": ",type(sample[key].values[0]),':',sample[key].values[0])

    



#load the used datasets
#data=pd.read_csv('instaPosts.csv')
#open .dta file
#data = pd.read_stata('Insta_posts_Mars2023.dta')
#data['preciseDate'] = pd.to_datetime(data['post_hour'],unit='ms')
#data['hour'] = data['preciseDate'].dt.hour

data=pd.read_csv('backuptweets2023.csv')
#convert date from string
data['Date'] = pd.to_datetime(data['Date'])
#get hour from date
data['hour'] = data['Date'].dt.hour


#print out some basic information about the database
statsOnDatabase(data)


def generateGraph1(data):
    #generate a graph that averages the number of likes per time of day
    
    engagement_by_hour = data.groupby('hour')['Likes'].mean()
    engagement_by_hour.plot(kind='bar')
    plt.title('Likes by Hour of Day (twitter)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Likes')
    plt.show()



def generateGraph2(data):
    #likes per day of week
    data['day_of_week'] = data['Date'].dt.day_name()

    engagement_by_day = data.groupby('day_of_week')['Likes'].mean()
    #reorder the days of the week
    engagement_by_day = engagement_by_day.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    engagement_by_day.plot(kind='bar')
    plt.title('Likes by Day (twitter)')
    plt.xlabel('Day')
    plt.ylabel('Likes')
    plt.show()

def generateGraph3(data):
    #likes per month
    data['month'] = data['Date'].dt.month_name()

    engagement_by_day = data.groupby('month')['Likes'].mean()
    #reorder the months
    engagement_by_day = engagement_by_day.reindex(['January', 'February', 'March', 'April', 'May', 'June', 'July','August','September','October','November','December'])
    engagement_by_day.plot(kind='bar')
    plt.title('Likes by Month (twitter)')
    plt.xlabel('Day')
    plt.ylabel('Likes')
    plt.show()



def generateGraph4(data):

    likes_by_newspaper = data.groupby('Newspaper')['Likes'].sum()*200
    views_by_newspaper = data.groupby('Newspaper')['Views'].sum()

    
    n=len(likes_by_newspaper)
    r = np.arange(n)
    width = 0.25
    

   
    plt.bar(r + width, likes_by_newspaper, color = 'g',
            width = width, edgecolor = 'black',
            label='Likes*200')

    plt.bar(r + width+width, views_by_newspaper, color = 'y',
            width = width, edgecolor = 'black',
            label='views')
    


    #legend each bar
    plt.xticks(r + width/2, likes_by_newspaper.keys(),rotation=90)
    plt.legend()
    plt.show()




def generateGraph5(data):
    #plots total number of subscribers vs likes/sub for each newspaper
    likes_by_newspaper = data.groupby('Newspaper')['Likes'].sum()
    #export likes by newspaper to flat array
    likes_by_newspaper=likes_by_newspaper.to_numpy()

    

    
    #divide arrays a and b element wise
    ratio=likes_by_newspaper/subsTwitter



    

    #scatter plot
    plt.scatter(subsTwitter,ratio)
    
    #label each point of the scatter
    for i, txt in enumerate(newspapersTwitter):
        plt.annotate(txt, (subsTwitter[i],ratio[i]))
    plt.show()
    plt.xlabel('Subs')
    plt.ylabel('Likes/Subs')




def countHashtags(str):
    #count the number of hashtags in a string
    count = 0
    for i in range(len(str)):
        if str[i] == '#':
            count += 1
    return count

def generateGraph7():
    #group tweets by number of hashtags

    data['hashtags'] = data['Text'].apply(countHashtags)

    #create a group of tweets with 0 to 5 hashtags
    data0=data[data['hashtags']==5]

    data1=data[data['hashtags']==1]
    data2=data[data['hashtags']==2]
    data3to5=data[data['hashtags'].between(3,5)]
    data6toinf=data[data['hashtags']>=6]

    #print length of each group
    print("0 hashtags: ",len(data0))
    print("1 hashtags: ",len(data1))
    print("2 hashtags: ",len(data2))
    print("3-5 hashtags: ",len(data3to5))
    print("6+ hashtags: ",len(data6toinf))

    #get the mean of likes for each group
    likes0=data0['Likes'].mean()
    likes1=data1['Likes'].mean()
    likes2=data1['Likes'].mean()
    likes3to5=data3to5['Likes'].mean()
    likes6toinf=data6toinf['Likes'].mean()

    #plot the results
    plt.bar(['0','1','2','3-5','6+'],[likes0,likes1,likes2,likes3to5,likes6toinf])
    plt.show()
    #legend the graph
    plt.xlabel('Number of hashtags')
    plt.ylabel('Mean Likes')
    plt.title('Mean Likes per number of hashtags (twitter)')


generateGraph7(data)
def generateGraph9(data,index):
    #generate a graph that averages the number of likes per time of day
    #index is the index of the newspaper in the array newspapersTwitter
    #data is the dataframe
    data=data[data['Newspaper']==newspapersTwitter[index]]
    engagement_by_hour = data.groupby('hour')['Likes'].mean()
    engagement_by_hour.plot(kind='bar')
    plt.title('Likes by Hour of Day (twitter) for '+newspapersTwitter[index])
    plt.xlabel('Hour of Day')
    plt.ylabel('Likes')
    plt.show()
#generateGraph9(data,0)

def generateGraph9bis(data,index):
    #generate a graph that shows the number of posts per time of day
    #index is the index of the newspaper in the array newspapersTwitter
    #data is the dataframe
    data=data[data['Newspaper']==newspapersTwitter[index]]
    engagement_by_hour = data.groupby('hour')['Newspaper'].count()
    engagement_by_hour.plot(kind='bar')
    plt.title('Number of posts by Hour of Day (twitter) for '+newspapersTwitter[index])
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of posts')
    plt.show()



def extractHashtags(s):
    #extract the hashtags from a string
    hashtags = []
    for word in s.split():
        if word[0] == '#':
            hashtags.append(word)
    return hashtags

def mostCommonHashtags(data,index):
    #Index is the newspaper's index in the array newspapersTwitter
    #data is the dataframe
    data=data[data['Newspaper']==newspapersTwitter[index]]
    #get the 10 most common hashtags used by the newspaper
    data['hashtags'] = data['Text'].apply(extractHashtags)
    hashtags = data['hashtags'].sum()
    hashtags = pd.Series(hashtags)
    hashtags = hashtags.value_counts()
    hashtags = hashtags[:10]
    return hashtags

#write in a single txt file the most common hashtags for each newspaper in the array newspapersTwitter
def writeHashtags(data):
    f = open("hashtags.txt", "w")
    for i in range(len(newspapersTwitter)):
        f.write("the newspaper is " + newspapersTwitter[i])

        f.write(str(mostCommonHashtags(data,i)))
        
        f.write("\n")
        f.write("\n")

#writeHashtags(data)



def getVeryLikedPosts(data,index):
    #gets the posts with more likes/subs than average for a newspaper
    #calculates the average likes/subs for the newspaper
    factor=50

    data=data[data['Newspaper']==newspapersTwitter[index]]
    likes=data['Likes'].mean()

    subs=subsTwitter[index]

    average=likes/subs

    #get the posts with more likes/subs than average
    data=data[data['Likes']>average*subs*factor]

    #write to file the data
    f = open("veryLikedPosts.txt", "w")
    f.write("the newspaper is " + newspapersTwitter[index])
    f.write("\n")
    f.write("\n")
    #write out the data exhaustively
    for i in range(len(data)):
        #loop on every column
        for j in range(len(data.columns)):
            f.write(str(data.columns[j]) + " : " + str(data.iloc[i,j]))
            f.write("\n")

        f.write("\n")
        f.write("\n")

getVeryLikedPosts(data,0)