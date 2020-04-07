{% load static %}
<?php
	
	extract($_GET);
	//$desc = array("Image1","Image2","Image3");
	$images = array("{% static 'budget_app/costs.png' %}","{% static 'budget_app/costs.png' %");
	$output = $images[$id-1];
	echo $output;

?>