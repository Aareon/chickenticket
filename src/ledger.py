import platform
import sys
import getpass
import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils import slog

# get file path of '.chickenticket' folder
system = platform.system()
if system == 'Windows':
    fore = 'C:\\Users\\{}\\AppData\\Local'.format(getpass.getuser())
else:
    fore = '~'

fp = '{}\\.chickenticket'.format(fore)
if not os.path.exists(fp+'\\logs'):
    os.makedirs(fp+'\\logs')

if not os.path.exists(fp+'\\ledger'):
    os.makedirs(fp+'\\ledger')

logger = slog.getLogger('{}\\wallet.log'.format(fp), level_input='DEBUG', terminal_output=True)

Base = declarative_base()

class Ledger(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, nullable=False)
    height = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)
    address = Column(String(length=64), nullable=False)
    recipient = Column(String(length=64), nullable=False)
    amount = Column(Integer, nullable=False)
    signature = Column(String, nullable=False) # signing key used to sign the transaction (PKCS1_v1_5)
    public_key = Column(String(length=88), nullable=False)
    block_hash = Column(String, nullable=False, unique=True)
    fee = Column(Integer, nullable=False)
    reward = Column(Integer, nullable=False)
    openfield = Column(String, nullable=True)

    def __repr__(self):
        return '<Transaction(id=\'{}\', height=\'{}\', timestamp=\'{}\', address=\'{}\', recipient=\'{}\', amount=\'{}\', signature=\'{}\', public_key=\'{}\', block_hash=\'{}\', fee=\'{}\', reward=\'{}\', openfield=\'{}\')>'.format(
            self.id, self.height, self.timestamp, self.address,
            self.recipient, self.amount, self.signature, self.public_key,
            self.block_hash, self.fee, self.reward, self.openfield
        )

    def _todict(self):
        return {
            "id": self.id,
            "height": self.height,
            "timestamp": self.timestamp,
            "address": self.address[:18],
            "recipient": self.recipient[:18],
            "amount": Decimal(self.amount/100000000),
            "signature": self.signature.decode()[:18],
            "public_key": self.public_key.decode()[:18],
            "block_hash": self.block_hash[:18],
            "fee": self.fee,
            "reward": self.reward,
            "openfield": self.openfield
        }

def load_ledger():
    logger.info('Creating ledger database engine...')
    try:
        engine = create_engine('sqlite:///{}\\ledger\\ledger.db?check_same_thread=False'.format(fp), echo=False)
        logger.info('Loaded `ledger.db`')
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        return session
    except:
        logger.warning('Failed to load `ledger.db`, exiting...')
        return None

if __name__ == "__main__":


    from decimal import Decimal, getcontext

    getcontext().prec = 8

    ledger = load_ledger()
    if not ledger:
        print("Unable to open records")
        logger.error("Failed to open ledger record")
        sys.exit(1)

    for transaction in ledger.query(Ledger).all():
        print(
"""------------------------
ID         : {id}
Height     : {height}
Time       : {timestamp}
Address    : {address}
Recipient  : {recipient}
Amount     : {amount} CHKN
Signature  : {signature}
Public Key : {public_key}
Hash       : {block_hash}
Fee        : {fee}
Reward     : {reward}
Openfield  : {openfield}
------------------------

""".format(**transaction._todict()))
