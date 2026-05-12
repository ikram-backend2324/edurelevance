from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AIEvaluation
from apps.nlp.extractor import extract_text
from apps.nlp.scorer import evaluate_relevance_with_lang


@login_required
def evaluate_view(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name', '').strip()
        topic_name = request.POST.get('topic_name', '').strip()
        topic_description = request.POST.get('topic_description', '').strip()
        resource_type = request.POST.get('resource_type', 'text')
        resource_title = request.POST.get('resource_title', '').strip()
        resource_url = request.POST.get('resource_url', '').strip()
        resource_text = request.POST.get('resource_text', '').strip()
        language = request.POST.get('language', 'uz')

        # Basic validation
        errors = []
        if not subject_name:
            errors.append('subject')
        if not topic_name:
            errors.append('topic')
        if not topic_description:
            errors.append('description')
        if not resource_title:
            errors.append('title')
        if resource_type == 'url' and not resource_url:
            errors.append('url')
        if resource_type == 'text' and not resource_text:
            errors.append('text')
        if resource_type == 'pdf' and not request.FILES.get('resource_file'):
            errors.append('pdf')

        if errors:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'ai_eval/evaluate.html', {
                'errors': errors,
                'post': request.POST,
            })

        # Create evaluation record
        evaluation = AIEvaluation(
            user=request.user,
            subject_name=subject_name,
            topic_name=topic_name,
            topic_description=topic_description,
            resource_type=resource_type,
            resource_title=resource_title,
            resource_url=resource_url if resource_type == 'url' else None,
            resource_text=resource_text if resource_type == 'text' else '',
            language=language,
        )

        # Extract text
        try:
            if resource_type == 'pdf':
                uploaded_file = request.FILES['resource_file']
                raw = extract_text(file=uploaded_file)
            elif resource_type == 'url':
                raw = extract_text(url=resource_url)
            else:
                raw = resource_text
            evaluation.raw_text = raw
        except Exception as e:
            evaluation.raw_text = resource_text

        evaluation.save()

        # Run AI evaluation
        try:
            result = evaluate_relevance_with_lang(
                topic_name=topic_name,
                topic_description=topic_description,
                resource_title=resource_title,
                resource_text=evaluation.raw_text,
                language=language,
            )
            evaluation.score = result['score']
            evaluation.label = result['label']
            evaluation.reason = result['reason']
            evaluation.key_matches = result.get('key_matches', [])
            evaluation.missing_topics = result.get('missing', [])
            evaluation.save()
            return redirect('ai_eval:result', pk=evaluation.pk)
        except Exception as e:
            messages.error(request, f'AI evaluation error: {str(e)}')
            evaluation.delete()
            return render(request, 'ai_eval/evaluate.html', {'post': request.POST})

    return render(request, 'ai_eval/evaluate.html')


@login_required
def result_view(request, pk):
    evaluation = get_object_or_404(AIEvaluation, pk=pk, user=request.user)
    return render(request, 'ai_eval/result.html', {'evaluation': evaluation})


@login_required
def history_view(request):
    evaluations = AIEvaluation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ai_eval/history.html', {'evaluations': evaluations})


@login_required
def delete_evaluation(request, pk):
    evaluation = get_object_or_404(AIEvaluation, pk=pk, user=request.user)
    evaluation.delete()
    return redirect('ai_eval:history')