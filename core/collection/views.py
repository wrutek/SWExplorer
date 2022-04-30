import os
from datetime import datetime

from django.conf import settings
from django.views.generic import ListView, View
from django.shortcuts import redirect, render

from . import config
from .api import get_request
from .models import Dataset

import petl as etl

from .processors import process_swe_data


class IndexView(ListView):
    """list of datasets"""
    template_name = 'collection/collections.html'
    model = Dataset


class FetchView(View):
    """actiont view for fetchin new dataset from swapi"""
    def get(self, request, *args, **kwargs):
        next_url = config.SWAPI_URL
        timestamp = datetime.now().timestamp()
        file_path = os.path.join(settings.MEDIA_ROOT, f'{timestamp}.csv')
        # first batch of data should write a header to csv file
        write_header = True
        mapped_homeworlds = {}
        while next_url:
            response = get_request(next_url)
            next_url = response.get('next')
            ppls = response.get('results')
            # process data
            processed, mapped_homeworlds = process_swe_data(ppls, mapped_homeworlds)
            etl.appendcsv(processed, file_path, write_header=write_header)
            write_header = False
        # todo: right now tz is not taken into account
        Dataset.objects.create(timestamp=timestamp, path=file_path)
        return redirect(request.GET.get('next', '/'))


class DetailsView(View):
    def get(self, request, *args, **kwargs):
        page_size = int(request.GET.get('page_size', 10))
        page_size = page_size if page_size > 0 else 10
        dataset_id = kwargs.get('dataset_id')
        dataset = Dataset.objects.get(id=dataset_id)
        data = etl.fromcsv(dataset.path)
        show_more = False
        if page_size < len(data):
            show_more = True
        return render(
            request,
            'collection/details.html',
            {
                'dataset': etl.data(data)[:page_size],
                'headers': etl.header(data),
                'page_size': page_size + 10,
                'dataset_id': dataset_id,
                'show_more': show_more,
            },
        )


class ValueCountView(View):
    def get(self, request, *args, **kwargs):
        dataset_id = kwargs.get('dataset_id')
        group_by = set((request.GET.get('group_by', 'name') or 'name').split(','))
        dataset = Dataset.objects.get(id=dataset_id)
        data = etl.fromcsv(dataset.path)
        grouped = data.valuecounts(*group_by)
        grouped = grouped.cutout('frequency')
        return render(
            request,
            'collection/value_count.html',
            {
                'grouped': etl.data(grouped),
                'all_headers': etl.header(data),
                'headers': etl.header(grouped),
                'dataset_id': dataset_id,
                'group_by': group_by,
            },
        )
