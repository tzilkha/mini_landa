import React from 'react';

const OfferTable = props => {
  return (
    <ul className="offers">
      {props.offers.map(offer => (offer.user +' - '+ offer.price))}
    </ul>
  );
};

export default OfferTable;
