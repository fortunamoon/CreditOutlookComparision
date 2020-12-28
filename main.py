import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Card:
    def __init__(self, name, apr, balance):
        self.name = name
        self.apr = apr
        self.balance = balance

    def daily_apr(self):
        return (self.apr/100) / 365

    def daily_interest(self):
        return self.daily_apr() * self.balance

    def monthly_interest(self):
        return self.daily_interest() * 30

    def rollover_balance(self):
        return self.monthly_interest() + self.balance

    def __str__(self):
        return self.name


def plot_data(df, note):
    ax = plt.gca()
    # ax.set_title(f'{card.name} paid in {month} months')
    df.plot(kind='line', x='Month', y='Total_Interest', ax=ax)
    df.plot(kind='line', x='Month', y='Balance', color='red', ax=ax)
    ax.text(4, 40,
            f'{note}',
            style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    plt.show()


def plot_data_summary(df, note):
    df2 = df.pivot(index='Month', columns='Card', values='Total_Interest')
    df = df.pivot(index='Month', columns='Card', values='Balance')
    ax = df2.plot()
    df.plot(kind='bar', ax=ax)
    ax.set_title('Card Comparison')
    ax.set_ylabel('Total Interest in $')
    ax.set_xlabel('Months')
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
    plt.savefig('Summary_Graph.svg')
    plt.show()


def run_scenario(card, paymemt_percent, min_payment):
    month = 0
    total_interest = 0
    df_data = pd.DataFrame(columns=('Card', 'Month', 'Interest', 'Balance', "Total_Interest"))

    while card.balance > 0:
        if card.balance * (paymemt_percent / 100) < min_payment:
            card.balance = card.balance - min_payment
        else:
            card.balance = card.balance - (card.balance * (paymemt_percent / 100))
        new_interest = card.monthly_interest()
        total_interest += new_interest
        new_balance = card.rollover_balance()
        df_data.loc[month] = [card.name] + [month] + [new_interest] + [new_balance] + [total_interest]
        month+=1
    note = f'It took {month} months to pay off your {card.name} and you paid ${round(total_interest, 2)} in interest'
    plot_data(df_data, note)

    return df_data


def collector():
    try:
        card_name = input('Welcome, please enter the name of your credit card:')
        card_interest = float(input(f'Please enter the {card_name}s interest rate:'))
        card_balance = float(input(f'Please enter the current balance for the {card_name}'))
        payment_percentage = float(input('Please enter the percentage of the balance you wish to pay every month or press enter for 2%:') or 2)
        minimum_payment = float(input(f'Please enter the minimum payment you wish to pay every month if {payment_percentage}% is to small') or 25)
        payment_amount = card_balance * (payment_percentage / 100)
        loaded_card = Card(card_name, card_interest, card_balance)
        df_scenario_data = run_scenario(loaded_card, payment_percentage, minimum_payment)
        run_another = input('Would you like to run another scenario? Y/N')

        return 1, df_scenario_data, run_another
    except ValueError as e:
        return e


if __name__ == '__main__':
    success = collector()
    df_summary = pd.DataFrame(columns=('Card', 'Month', 'Interest', 'Balance', "Total_Interest"))
    if success[0] == 1:

        while success[2].lower() =='y':
            df_summary = df_summary.append(success[1])
            success = collector()
        df_summary = df_summary.append(success[1])
        to_compare = input('Would you like to compare the cards? Y/N:')
        if to_compare.lower() == 'y':
            plot_data_summary(df_summary, 'Summary')
    else:
        print('\n*******************************')
        print(f'\nThere is a problem, {success}')







