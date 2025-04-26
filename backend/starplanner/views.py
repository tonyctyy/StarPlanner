from django.shortcuts import render, redirect


def home(response):
    return redirect('coaching/profile')