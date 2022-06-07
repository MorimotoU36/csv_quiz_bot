// A utility function to create HTML.
function getHtml(template) {
    return template.join("\n");
}

function addImage(aws_config) {
    // bucket name.
    var bucketName = aws_config.s3.bucketName;

    // config, cognito
    AWS.config.region = aws_config.config.region; // Region
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
        IdentityPoolId: aws_config.cognito.IdPool_id,
    });

    // Create a new service object
    var s3 = new AWS.S3({
        apiVersion: "2006-03-01",
        params: { Bucket: bucketName },
    });

    var files = document.getElementById("fileInput").files;
    if (!files.length) {
        return set_error_message("Please choose a file to upload first.");
    }
    var file = files[0];
    var photoKey = file.name;

    // Use S3 ManagedUpload class as it supports multipart uploads
    var upload = new AWS.S3.ManagedUpload({
        params: {
            Bucket: bucketName,
            Key: photoKey,
            Body: file
        }
    });

    var promise = upload.promise();

    promise.then(
        function (data) {
            set_message("Successfully uploaded image.");
        },
        function (err) {
            return set_error_message("There was an error uploading your image: ", err.message);
        }
    );
}

