function Login(props) {

  const formSubmitHandler = event => {
    // Dont reload
    event.preventDefault();

    // Get form input
    var input = event.target[0].value

    // Check its not whitespaces and send to App
    if (input.trim().length > 0) {
      props.onEnter(input)
    };
  };

  return (
    <form onSubmit={formSubmitHandler}>
      <div>
        <label >Username: </label>
        <input type="text"/>
      </div>
      <button type="submit">Enter</button>
    </form>
  );
}

export default Login;