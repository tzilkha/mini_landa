import './App.css';
import React, { useState } from 'react';
import Login from './components/Login.js';
import BuySell from './components/BuySell.js';
import OfferTable from './components/OfferTable.js';


function App() {
  const [username, setUsername] = useState("");
  const [stocks, setStocks] = useState(0);
  const [loggedIn, setLoggedIn] = useState(false);

  const[buyoffers, setBuyOffers] = useState([{'user':'fakebuy', 'price':0.01}]);
  const[selloffers, setSellOffers] = useState([{'user':'fakesell', 'price':0.01}]);

  function loginHandler(_username) {
    setUsername(_username);
    setLoggedIn(true);

    // API CALL TO LOG IN

  }

  function createOfferHandler(isbuy, price){
    console.log(isbuy, price);

    //API CALL TO MAKE OFFER

    return;
  }


  return (
    <div>
    {loggedIn? <div className="App-banner">{'Logged in as: '+username}</div>: null}
    {loggedIn? <div className="App-banner">{'Stocks Owned: '+stocks}</div>: null}

      <div className="App">
        <header className="App-header">
          {!loggedIn ? <Login onEnter={loginHandler}/>: null}
          {loggedIn ? <BuySell onEnter={createOfferHandler}/>: null}
        </header>
      </div>

    {/* {loggedIn ? */}
    {/*   <div><div className="App-buysell"> */}
    {/*     Buy Offers */}
    {/*     <OfferTable offers={buyoffers}/> */}
    {/*   </div> */}
    {/*   <div className="App-buysell"> */}
    {/*     Sell Offers */}
    {/*     <OfferTable offers={selloffers}/> */}
    {/*   </div> </div>: null */}
    {/* } */}
    
    </div>
  );
}

export default App;
