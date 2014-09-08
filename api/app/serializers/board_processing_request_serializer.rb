class BoardProcessingRequestSerializer < ActiveModel::Serializer

  attributes :id, :submitted_at, :started_at, :completed_at, :result

  def filter(keys)
    keys.delete(:submitted_at) unless object.submitted?
    keys.delete(:started_at) unless object.started?
    keys.delete(:completed_at) unless object.completed?
    keys.delete(:result) unless object.completed?
    keys
  end


end
