import time
import pandas as pd
import numpy as np
from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#MONTHS and DAYS List will be used by multiple functions and will not be changed
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june','all']
DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input("From which City do you want the data? (chicago, new york city, washington) ")
        city=city.lower()
        if (city in CITY_DATA)==False:
            print('Please select a city that exists in the database')
        else:
            break
         
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("For which Month do you want the data? (all, january, february, ... , june)")
        month=month.lower()
        if (month in MONTHS)==False:
            print('Please select a month that exists')
        else: 
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("For which Day do you want the data? (all, monday, tuesday, ... , sunday)")
        day=day.lower()
        if (day in DAYS)==False:
            print('Please select a day that exists')
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # create month column
    df['month'] = df['Start Time'].dt.month
    
    # create date column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df.month.eq(month)]
    
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week.eq(day.capitalize())]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # create a list of the most common months which holds only the most common month
    most_common_month=df['month'].value_counts()[:1].index.tolist()
    #get the first and only int element of the most_common_month list and use it as index of the MONTHS List 
    print('The most common Month is: ',MONTHS[most_common_month[0]-1])

    # TO DO: display the most common day of week
    most_common_day=df['day_of_week'].value_counts()[:1].index.tolist()
    print('The most common day is: ',most_common_day[0])
    
    # TO DO: display the most common start hour
    hours = df['Start Time'].dt.hour
    most_common_start_hour=hours.value_counts()[:1].index.tolist()
    
    print('The most common Start Hour is: ',most_common_start_hour[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    print('The most commonly used start station is: ',df['Start Station'].value_counts()[:1].index.tolist())

    # TO DO: display most commonly used end station
    print('The most commonly used end station is: ', df['End Station'].value_counts()[:1].index.tolist())


    # TO DO: display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station is: ',df.groupby(['Start Station','End Station']).size().idxmax())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    #Get the sum/mean of all seconds in the dataframe column and covert it to python Type int
    summed_seconds=df['Trip Duration'].sum().item()
    mean_seconds=df['Trip Duration'].mean().item()

    #format the time to a readable format using the datetime package
    summed_seconds_formatted = timedelta(seconds=summed_seconds)
    mean_seconds_formatted = timedelta(seconds=mean_seconds)

    # TO DO: display sum travel time
    print('Neue Berechnung: The total travel Time was: ',summed_seconds_formatted, ' (hours, minutes, seconds)')
   
    # TO DO: display mean travel time
    print('Neue Berechnung The mean travel Time was: ', mean_seconds_formatted, '(hours, minutes, seconds)')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    # TO DO: Display counts of user types
    print('User Typs\n', df['User Type'].value_counts(), '\n')

    
    #perform the Gender and Birth count only if the city is new york or chicago. Washington does not have these columns
    if city=='new york city' or city=='chicago':
        # TO DO: Display counts of gender
        print('Gender \n', df['Gender'].value_counts(), '\n')

        # TO DO: Display earliest, most recent, and most common year of birth
        print('Most recent year of birth: ', int(df['Birth Year'].max()))
        print('Earliest year of birth: ', int(df['Birth Year'].min()))
    
        most_common_year=df['Birth Year'].mode()
        print('Most common year of birth: ',  int(most_common_year[0]))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    counter=5
    while True:
        
        if counter == 5:
            answer = input("Do you want to see 5 rows of raw data? (yes/no) ")
            answer = answer.lower()
        else:
            answer = input("Do you want to see more raw data? (yes/no) ")
            answer = answer.lower()
            
        if(answer=='yes'):
            print(df[counter-5:counter])
            counter+=5
           
        elif(answer=='no'):
            break
 

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
	main()
