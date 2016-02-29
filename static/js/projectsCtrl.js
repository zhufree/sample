var proApp = angular.module('proApp', []);

proApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});
proApp.controller('tagCloud', ['$scope', function($scope){
  $scope.words = [
    {name: 'python', size: Math.random() * 10 + 1},
    {name: 'django', size: Math.random() * 10 + 1},
    {name: 'flask', size: Math.random() * 10 + 1},
    {name: 'html', size: Math.random() * 10 + 1},
    {name: 'css', size: Math.random() * 10 + 1},
    {name: 'javascript', size: Math.random() * 10 + 1},
    {name: '数据结构', size: Math.random() * 10 + 1},
    {name: '算法', size: Math.random() * 10 + 1},
    {name: '教育', size: Math.random() * 10 + 1},
    {name: '互联网', size: Math.random() * 10 + 1},
    {name: '编程', size: Math.random() * 10 + 1},
    {name: '信息管理', size: Math.random() * 10 + 1},
    {name: '数字出版', size: Math.random() * 10 + 1},
    {name: '篮球', size: Math.random() * 10 + 1},
    {name: 'free', size: Math.random() * 10 + 1},
    {name: 'WHU', size: Math.random() * 10 + 1},
    {name: '柚子君', size: Math.random() * 10 + 1},
  ];
  // console.log($scope.words);
}]);
