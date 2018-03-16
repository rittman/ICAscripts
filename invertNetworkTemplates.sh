for i in ~/Functional_ROIs/*/*.nii.gz ; do
 echo $i
 fslmaths $i -div $i -sub 1 -mul -1 ${i/.nii.gz/_inv.nii.gz}
done
