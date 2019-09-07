import React, { Component } from "react";

class Login extends Component {

    render() {
        return (
            <form className="form-group">
                <div>
                    <h3>Choose username to start playing</h3>
                    <input type="text" placeholder="username" className="form-control" />
                    <input type="password" placeholder="password" className="form-control" />
                </div>
            </form>
        )
    }
}


export default Login