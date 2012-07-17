$(function(){
  $('.pager a').click(function(e){
    e.preventDefault();
    var t = $(this);
    if (t.parent().hasClass('disabled')) return;

    var url = new URI(document.location.href);
    var pg = URI.parseQuery(url.search())['pg'];
    if (pg) pg = parseInt(pg);
    else pg = 1;

    if (t.hasClass('next')) pg += 1;
    else pg -= 1;

    url.removeSearch('pg');
    if (1 != pg) url.addSearch('pg', pg);

    document.location.href = url.normalize();
  });

  $('form.search').submit(function(e){
    e.preventDefault();
    document.location.href = '/search/' + encodeURIComponent(
      $(this).find('.search-query')[0].value);
  });
});
