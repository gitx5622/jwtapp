import React, { Component, Fragment }from 'react';
import { BrowserRouter as Router,Switch,Route} from "react-router-dom";
import { connect } from 'react-redux';
import * as actions from './store/actions/auth';

import Login from './accounts/Login';
import Signup from './accounts/Signup';

class App extends Component {
  
  componentDidMount (){
    this.props.onTryAutoSignup();
  }

render(){
  return(
    <Router>
    <Fragment>
      <Switch>
        <Route exact path= '/login' component={Login} />
        <Route exact path= '/signup' component={Signup} />
      </Switch>
    </Fragment>
  </Router>
  )};

}
const mapStateToProps = state => {
  return {
    isAuthenticated: state.token !== null
    }
  }
  const mapDispatchToProps = dispatch => {
    return {
      onTryAutoSignup: () => dispatch(actions.authCheckState())
        }
    }
  
export default connect(mapStateToProps, mapDispatchToProps)(App);
  