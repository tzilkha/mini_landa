import './BuySell.css';
import React, { useState } from 'react';

function BuySell(props) {
  const [isBuy, setIsBuy] = useState(true);

  function formSubmitHandler(event){
    // Dont reload
    event.preventDefault();

    // Get form input
    var input = event.target[0].value

    // Send to App offer
    props.onEnter(isBuy, input)

  };

  function radioChangeBuy(){
    setIsBuy(true);
  }

  function radioChangeSell(){
    setIsBuy(false);
  }

  return (
    <div>
      <form onSubmit={formSubmitHandler}>
        <div>
          <label >Price: </label>
          <input type="number" min="0.00" max="10000.00" step="0.01" defaultValue={0}/>
        </div>
        <input type="radio" name='buyorsell' value='buy' checked onChange={radioChangeBuy}/>Buy
        <input type="radio" name='buyorsell' value='sell' onChange={radioChangeSell}/>Sell
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>   
    </div>

  );
}

export default BuySell;