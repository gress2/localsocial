define([
	'components/search-service.js',
	'top-nav/search-bar/quick-results/quick-results-component',
	'react'
], function(
	SearchService,
	QuickResultsComponent,
	React
) {
	var SearchBar = React.createClass({
		getInitialState() {
			return {
				results: [],
			}
		},
		render() {
			return <div className="search-bar">
				<input type="text" placeholder="Search" onChange={this.updateSearchQuery} />
				<button>Go</button>
				<QuickResultsComponent results={this.state.results} />
			</div>;
		},
		updateSearchQuery(event) {
			var query = event.target.value;

			SearchService.search(query).then((response) => {
				this.setState({
					results : response.results
				});
			});
		}
	});

	return SearchBar;
});