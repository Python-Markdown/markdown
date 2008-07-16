This should be stripped/escaped in safe_mode.

<script>
alert("Hello world!")
</script>

With blank lines.

<script>

alert("Hello world!")

</script>

Now with some weirdness

``<script <!--
alert("Hello world!")
</script <>`` `

Try another way.

<script <!--
alert("Hello world!")
</script <>

This time with blank lines.

<script <!--

alert("Hello world!")

</script <>
