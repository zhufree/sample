var proApp = angular.module('proApp', []);

proApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});
proApp.controller('showPro', ['$scope', function($scope){
  $scope.pros = [
    {name: 'TagCloud', desc: '随机位置大小和颜色的标签云',
      imgLink: 'http://7xlfws.com1.z0.glb.clouddn.com/1395922265.jpg',
      link: 'http://codepen.io/zhufree/full/xVbrrJ/'},
    {name: 'FoodShop', desc: '食物商品展示单页面应用，可以添加商品',
      imgLink: 'http://7xlfws.com1.z0.glb.clouddn.com/foodshop2016-03-01T06-54-05.448Z.png',
      link: 'http://codepen.io/zhufree/full/ZWYyJX/'}
  ];
}]);
