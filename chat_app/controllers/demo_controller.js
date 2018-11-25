// Export functions for our routes.js file to use. This is where the logic of
// your server will go.
module.exports = {

  home_function: function(req, res){
    res.render('index');
  }

}
