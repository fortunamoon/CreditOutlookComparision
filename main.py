import pandas as pd
import matplotlib.pyplot as plt


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


def run_scenario(card, paymemt_percent):
    month = 0
    total_interest = 0
    df_data = pd.DataFrame(columns=('Month', 'Interest', 'Balance', "Total_Interest"))

    while card.balance >0:
        card.balance = card.balance - (card_balance * (paymemt_percent / 100))
        new_interest = card.monthly_interest()
        total_interest += new_interest
        new_balance = card.rollover_balance()
        df_data.loc[month] = [month] + [new_interest] + [new_balance] + [total_interest]
        month+=1
    ax = plt.gca()
    # ax.set_title(f'{card.name} paid in {month} months')
    df_data.plot(kind='line', x='Month', y='Total_Interest', ax=ax)
    df_data.plot(kind='line', x='Month', y='Balance', color='red', ax=ax)
    ax.text(4, 40, f'It took {month} months to pay off your {card.name} and you paid ${round(total_interest,2)} in interest', style='italic',
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    plt.show()


if __name__ == '__main__':
    card_name = input('Welcome, please enter the name of your credit card:')
    card_interest = float(input(f'Please enter the {card_name}s interest rate:'))
    card_balance = float(input(f'Please enter the current balance for the {card_name}'))
    payment_percentage = float(input('Please enter the percentage of the balance you wish to pay every month or press enter for 2%:') or 2)
    payment_amount = card_balance * (payment_percentage / 100)
    loaded_card = Card(card_name, card_interest, card_balance)
    run_scenario(loaded_card, payment_percentage)





