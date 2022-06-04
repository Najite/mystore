const form = document.getElementById('payform');
form.addEventListener('submit', makePayment);

function makePayment() {
    FlutterwaveCheckout({
      public_key: "FLWPUBK_TEST-SANDBOXDEMOKEY-X",
      tx_ref: "jumla" + Math.floor((Math.random() *10000000) + 1),
      amount: document.getElementById('amount').value,
      currency: "NGN",
      payment_options: "card",
      redirect_url: "http://127.0.0.1:8000",
    
      customer: {
        email: document.getElementById('email').value,
        phone_number: document.getElementById('phone').value,
        name: document.getElementById('name'.value),
      },
      customizations: {
        title: "Jumla Store",
        description: "Payment for ordered items",
      },
      
      data:{
          cardno: document.getElementById('cardno').value,
          cvv:document.getElementById('cvv').value,
          expirymonth: document.getElementById('expiry').value,
          expiryyear:document.getElementById('year'),

      }
    });
  }