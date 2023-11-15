<template>
    <section id="hero" class="hero d-flex align-items-center">
    <div class="container">
        <router-view class="d-flex flex-column justify-content-center" />
    </div>
    </section>
</template>


<style scoped>

@media (min-height: 101vh) {
    #hero .container{
        padding-top: 20vh;
    }
}
</style>