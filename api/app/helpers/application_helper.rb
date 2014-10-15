module ApplicationHelper

  def title(page_title)
    content_for(:title) { page_title }
  end

  def og(p={})
    key, value = p.symbolize_keys!.first
    content_for("og:#{key}") { value }
  end
end
