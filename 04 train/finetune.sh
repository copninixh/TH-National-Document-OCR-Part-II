rm -rf output/*
OMP_THREAD_LIMIT=8 lstmtraining \
    --continue_from tha.lstm \
    --model_output output/thnd \
    --traineddata tesseract/tessdata/tha.traineddata \
    --train_listfile train/tha.training_files.txt \
    --max_iterations 1000