ko.validation.init({
    registerExtenders: true,
    messagesOnModified: true,
    insertMessages: true,
    parseInputAttributes: true,
    errorClass: 'errorStyle',
    messageTemplate: null
}, true);

(function () {
    var viewModel = function () {
        var self = this;
		var client_data;
		$.ajax({
			type: 'GET',
			url: '/clients',
			contentType: "application/javascript",
			dataType: "json",
			async:false,
			success: function (data) {
				client_data = data;
			},
			error: function (jq, st, error) {
				if(error=="Unauthorized"){
					window.location.href = "/"
				}
			}
		});
		var product_data;
		$.ajax({
			type: 'GET',
			url: '/products',
			contentType: "application/javascript",
			dataType: "json",
			async:false,
			success: function (data) {
				product_data = data;
			},
			error: function (jq, st, error) {
				if(error=="Unauthorized"){
					window.location.href = "/"
				}
			}
		});
	
        var IsUpdatable = false;
        self.validateNow = ko.observable(false);
        self.Title = ko.observable().extend({  
            required: { message: 'Please enter title.' }
        }),
        self.Description = ko.observable();
        self.Client = ko.observableArray(client_data);
        self.ClientId = ko.observable().extend({
            required: { message: 'Please select client.' }
        }),
        self.ClientPriority = ko.observable().extend({
            required: { message: 'Please select priority.' }
        }),
        self.TargetDate = ko.observable().extend({
							required: { message: 'Please select target date.' }, 
							validation: {
								validator: function (val) {
									val = val.replace(/-/g,'/')
									return new Date(val) > new Date();
								},
								message: "Target date should be greater than today's date",
							}
						});
        self.ProductArea = ko.observableArray(product_data);
        self.ProductAreaId = ko.observable().extend({
            required: { message: 'Please select product.' }
        }),
        self.errors = ko.validation.group(self);

        var RequisitionInfo = {
            title: self.Title,
            desc: self.Description,
            client_id: self.ClientId,
            priority: self.ClientPriority,
            target_date: self.TargetDate,
            product_id : self.ProductAreaId
        };

        self.Requisitions = ko.observable([]);
            
        loadInformation();

        function loadInformation() {
			var parsedData;
			$.ajax({
				type: 'GET',
				url: 'requests',
				contentType: "application/javascript",
				dataType: "json",
				async:false,
				cache:false,
				success: function (data) {
					parsedData = data;
				},
				error: function (jq, st, error) {
					if(error=="Unauthorized"){
						window.location.href = "/"
					}
				}
			});
	
			self.Requisitions = ko.observableArray(parsedData);
		
        }
		
        self.ClearValues = function()
        {
            self.Title(null);
            self.Description(null);
            self.ClientId(null);
            self.ClientPriority(null);
            self.TargetDate(null);
            self.ProductAreaId(null);
        }
        self.cross = function () {
            self.ClearValues();
            self.errors.showAllMessages(false);
        }
        self.cancel = function () {
            self.ClearValues();
            self.errors.showAllMessages(false);
        }

        self.save = function () {
            self.validateNow(true);
            if (self.errors().length === 0) {
				var json1 = ko.toJSON(RequisitionInfo);
				$.ajax({
					url: '/addrequest',
					type: 'POST',
					dataType: 'json',
					data: json1,
					contentType: 'application/json; charset=utf-8',
					success: function (data) {
						array_data = [data.request_id,
										data.title,
										data.desc,
										data.client_name,
										data.priority,
										data.target_date,
										data.product_area
									]
						$('#request_list').DataTable().row.add(array_data).draw(false);
						$('#btnCross').click();
					},
					error: function (jq, st, error){
						if(error=="Unauthorized"){
							window.location.href = "/"
						}
					}
				});
            }
            else
            {
                self.errors.showAllMessages();
                return;
            }
             
        }
    };
    ko.applyBindings(new viewModel());
})();
