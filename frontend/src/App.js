import React, { useState, useEffect } from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { useDispatch } from "react-redux";
import LoginForm from "./components/auth/LoginForm";
import SignUpForm from "./components/auth/SignUpForm";
import NavBar from "./components/NavBar";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import { authenticate } from "./store/session";
import HomePage from "./components/images/HomePage";
import Footer from "./components/footer/footer"

function App() {
	const [loaded, setLoaded] = useState(false);
	const dispatch = useDispatch();

	useEffect(() => {
		(async () => {
			await dispatch(authenticate());
			setLoaded(true);
		})();
	}, [dispatch]);

	if (!loaded) {
		return null;
	}

	return (
		<div>
			<BrowserRouter>
				<NavBar />
				<Switch>

					<Route
						path='/'
						exact={true}
					>
						<HomePage />
					</Route>

					<Route
						path='/login'
						exact={true}
					>
						<LoginForm />
					</Route>

					<Route
						path='/sign-up'
						exact={true}
					>
						<SignUpForm />
					</Route>

				</Switch>
			</BrowserRouter>
			<Footer />
		</div>
	);
}

export default App;
