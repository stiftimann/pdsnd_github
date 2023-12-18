import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n')
    print('-'*100)
    print('-'*100)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*100)
    print('-'*100)
    print('\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        # Start Text Cities:
        print("Please type in the name of one of the three citys for analyzing. Large and lower case doesn`t matter.\nTake care of the correct spelling of the cityname like 'Chicago', 'new York city' or 'WashinGTon'.")
        city_list = ['chicago', 'new york city','washington']
        city = str(input("Input Cityname: ")).lower() # correct input to lower case
        if city in city_list:
          print("Choosen Cityname: '{}'".format(city.title())) # correct to format 'title'
          break
        else:
            print("Error: Cityname '{}' is not correct.\nPlease try again check the correct spelling of the city.\n".format(city))

    # get user input for month (all, january, february, ... , june)
    while True:
        print("\nPlease choose the month to analyze only from 'January' to 'June' or type 'all' for all months.\nLarge and lower case doesn`t matter. Take care of the correct spelling of the month.")
        month_list = ['all', 'january','february','march','april','may','june']
        month = str(input("Input Month: ")).lower()
        if month in month_list:
            print("Choosen Month: '{}'".format(month.title()))
            break
        else: 
           print("Error: Month '{}' is not correct.\nPlease try again check the correct spelling of the month.".format(month))    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print("\nPlease choose the day to analyze only from 'Monday' to 'Sunday' or type 'all' for all days.\nLarge and lower case doesn`t matter. Take care of the correct spelling of the day.")
        day_list = ['all', 'monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
        day = str(input("Input Day: ")).lower()
        if day in day_list:
            if day == 'all':
                print("Choosen Day(s): '{}'".format(day)) # no '.title()' format for 'all 
                break 
            else:
                print("Choosen Day(s): '{}'".format(day.title()))
                break            
        else: 
           print("Error: Day '{}' is not correct.\nPlease try again check the correct spelling of the day.".format(day))   

    print('-'*100)
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
    print("\nPreparing data...")
    start_time = time.time()
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() # dt.weekday_name doesn`t work anymore

    # Filter Section - Month
    if month != 'all':
        # create new Integer column if filter set to month
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = month_list.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter Section - Month
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    # hows runtime for calculating
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

    #returns all selections as dataframe (df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month as iteger and as string
    month_list = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df['month'].mode()[0]
    print("The most common month is: '{}' ('{}')".format(common_month, month_list[common_month - 1].title()))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is: '{}'".format(common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common hour is: '{}'".format(common_hour))

    # hows runtime for calculating
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    commonly_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: '{}'.".format(commonly_start_station))

    # display most commonly used end station
    commonly_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: '{}'.".format(commonly_end_station))

    # display most frequent combination of start station and end station trip
    df['start_stop_combination'] = df['Start Station']+" "+"to"+" "+df['End Station']
    commonly_start_stop = df['start_stop_combination'].mode()[0]
    print("The most commonly Start-Stop-Combination is: '{}'.".format(commonly_start_stop))

    # hows runtime for calculating
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_sum =df['Trip Duration'].sum()
    trip_day = int(trip_sum / (60 * 60 * 24))
    trip_hour = int((trip_sum / (60 * 60)) - (trip_day * 24))
    trip_min = int((trip_sum / 60) - (trip_day * 24 * 60)) - (trip_hour * 60)
    trip_s = trip_sum - (trip_day * 60 * 60 * 24) - (trip_hour * 60 * 60) - (trip_min * 60)
    print("The total travel time is: '{}' day(s), '{}' hour(s), '{}' minutes(s) and '{}' second(s).".format(trip_day, trip_hour, trip_min, trip_s))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("The average trip duration is: '{:,.2f}' minutes.".format(mean_travel/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    for user_type in user_count.index:
        print("There are '{}' users of user-typ '{}'.".format(user_count[user_type], user_type))
    print('')
    
    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        for gender in gender_count.index:
            print("There are '{}' users with a gender '{}'.".format(gender_count[gender], gender))
    except:
        print("There are no 'gender data' of the customers in this dataset.")     

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nThe earlies year of birth is: '{}'\nThe most recent year of birth is: '{}'\nThe most common year of birth is: '{}'".format(earliest, most_recent, most_common))
    except:
        print("\nThere are no 'birth data' of the customers in this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def print_lines(df):
    """ Display the filtered Raw Data """

    print('\nDisplay RawData...\n')
    start_time = time.time()

    # needed for 'yes' 'no' question
    choice_list = ['yes', 'no']

    # User-Input for the 'first 5 Lines'
    while True:
        first_lines = input("Would you like to see the first 5 Lines? Enter 'yes' or 'no'.\nInput: ")
        print('')
        if first_lines.lower() in choice_list:
            break
        else:
            print("Error: Please answer with '{}' or '{}'.".format(choice_list[0], choice_list[1]))
    if first_lines.lower() != 'yes':
        return None

    # User-Input for the 'next 5 Lines'
    i = 1
    while i < len(df):
        print("Line: {} to Line: {}\nSortet by '[Start Time']\n".format(i, 5+i))
        print(df.sort_values(by=['Start Time'])[i:5+i])
        i += 5
        while True:
            next_lines = input("\nWould you like to see the next 5 Lines? Enter 'yes' or 'no'.\nInput: ")
            if next_lines.lower() in choice_list:
                break
            else:
                print("Error: Please answer with '{}' or '{}'.".format(choice_list[0], choice_list[1]))
        if next_lines.lower() != 'yes':
            break
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_lines(df)

        # needed for 'yes' 'no' question
        choice_list = ['yes', 'no']

        #restart procedure
        while True:
            restart = input("\nWould you like to restart? Enter 'yes' or 'no'.\nInput: ")
            if restart.lower() in choice_list:
                break
            else:
                print("Error: Please answer with '{}' or '{}'.".format(choice_list[0], choice_list[1]))
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
