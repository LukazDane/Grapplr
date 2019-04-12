# Grapplr

### Reason for starting this project?

Sometimes a good way to blow off steam, or just make a bad day better is to hit something. Typically running up to strangers and punching them in the jaw is frowned upon. Friends and kismet enemies may be up for a spar occasionally, but maybe you want some variety in your beat downs. This app is actually meant to be a way for those of us who are more tactile or have bottled up aggression to release that in a way that's fun, instinctual, and legal!

### Tech Used:

- Flask
- ~~Peewee~~
- SQLAlchemy
- Jinja
- Sqlite

##### Api's:

- Google Maps
- Google Places

### User Stories

    * Users can visit site to see a landing/sign-up page
    * Users can Login/Register
    * Users can post open fight requests on a dashboard, available for all users to see.
    * User can edit/delete open fight requests. (Title, Content, Location)
    * Users can see the number of challangers/users challanged on their profile.
    * Users are able to udate profile info.
    * Users are able to visit a grid page to see all other users and view their information.
    * User is able to send a challange request to another user.

## Unsolved Problems/Future Fixes

- Users can match with eachother, but sqlite will not return the information in a readable way
- Currently using prepopulated form to put matches into database. This can and should be done differently.
- Style overly that blocks desktop view to look more professional
- Submitting or editing fight requests rerouts to an error, but the requests do post and update appropriately
- Need to add user notification when users match eachother
- add logo
- deploy with kivy
- change grid back to swipe once jQuery thing is solved

### Code

I guess the only code i could say i'm kind of proud of is the user grid. Getting the grid to display user phots was tricky. Getting the grid to display the right ser photo was a mess.
![swipe](https://github.com/LukazDane/Grapplr/blob/master/static/CodeBlocks/user_grid.png)
![grid](https://github.com/LukazDane/Grapplr/blob/master/static/CodeBlocks/user_grid_route.png)

### Biggest Challanges

- Figuring out the association table for user to user matches. Each solution I found ended up creating a different problem.
- jQuery and Scripts won't/wouldn't work in js file.
- Docs for a lot of the things I needed were out of date.
- At one point data from challanges was populating to databases consitently and in trying to figure out why it would only return "generator x0002342348" objects, I couldn't backtrack to poplulate it the same way again.

### Successes

- Found a work around to get challanges/challanger into db with a form(not-ideal)

- Google Map auto fills, and adjusts to inut location on fightform

- all fights with a location tag link to a google maps page for that location

### Shoutouts

- Emily(TA) for doing her best to help me with my db issues.
- Jon for showing me how he did matches(even though i couldn't use it in time, it would work on a futre build)
