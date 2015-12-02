define(
	[
		'react',
		'components/post-service',
		'components/user-service',
		'home-feed/feed/feed-component', 
		'home-feed/post-form/post-form-component'
	], 
	function(
		React,
		PostService,
		UserService,
		Feed, 
		NewPostForm
	) {
		'use strict';

		var HomeFeed = React.createClass({
			getInitialState() {
				return {
					posts: [],
					pageNum : 0,
				};
			},
			componentWillMount() {
				this.getNewPosts();
			},
			render() {
				return (
					<div className="home-feed-area">
						<NewPostForm onSubmit={ this.submitPost } />
						<Feed posts={ this.state.posts } />
					</div>
				);
			},

			getNewPosts() {
				PostService.getPosts().then(
					(data) => {
						this.setState({ posts : data.posts });
					},
					(error) => {
						// TODO error state
						console.log("Error", error);
					}
				);
			},

			submitPost(newPost) {
				var locationOverride = UserService.getCustomLocation();

				if(locationOverride) {
					newPost.city = locationOverride.city;
					newPost.longitude = locationOverride.longitude;
					newPost.latitude = locationOverride.latitude;
				}

				PostService.savePost(newPost);

				this.getNewPosts();
			}
		});

		return HomeFeed;
});